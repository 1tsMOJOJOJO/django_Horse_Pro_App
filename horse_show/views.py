from django.template import Context
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.db import connection
from django.core import serializers
from horse_show.models import Show, ShowClass, ShowClassSchedule, Number, Rider, Entry, ClassEntry,\
                              EntryType, Division, Club
import csv, sqlite3, json, io

@require_http_methods(["GET"])
def index(request, show_id=None):
    '''
    Shows all loaded shows and allows the user to select one to manage
    '''
    show_list = Show.objects.all().order_by('-Date')
    show = None
    if show_id:
        show = Show.objects.get(pk=show_id)
    return render(request, 'index.html', context={'shows': show_list, 'show':show})

@require_http_methods(["GET"])
def list_classes(request, show_id):
    '''lists all classes in a show'''
    show = get_object_or_404(Show, pk=show_id)
    queryset = ShowClassSchedule.objects.filter(Show=show_id)
    return render(request, 'classes/class_list.html', context={'object_list':queryset, 'show':show})

@require_http_methods(["GET"])
def print_class(request, show_id, class_id):
    '''Provides a printable view of class sheets'''
    show = get_object_or_404(Show, pk=show_id)
    sc = get_object_or_404(ShowClass, pk=class_id)
    cursor = connection.cursor()
    cursor.execute("""SELECT n.Number FROM horse_show_number n
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s;""", [class_id, show_id])
    ring_rows = cursor.fetchall()

    cursor.execute("""SELECT n.Number, r.FirstName, r.LastName, n.HorseName, club.Name
        FROM horse_show_rider r
        INNER JOIN horse_show_club club ON club.id = r.Club_id
        INNER JOIN horse_show_number n ON r.id = n.Rider_id
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s;""", [class_id, show_id])
    announce_rows = cursor.fetchall()
    return render(request, 'classes/class_print.html', context={'ring':ring_rows, 'announcer':announce_rows, 'cls':sc})

@require_http_methods(["GET"])
def print_split_class(request, show_id, class_id):
    '''Provides a printable view of class sheets, split by Jr, Int. Sr.'''
    #show = Show(show_id)
    show = get_object_or_404(Show, pk=show_id)
    sc = get_object_or_404(ShowClass, pk=class_id)
    cursor = connection.cursor()
    cursor.execute("""SELECT n.Number FROM horse_show_number n
        INNER JOIN horse_show_rider r ON n.Rider_id = r.id
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s AND r.Division = "SENIOR"
        ORDER BY n.Number;""", [class_id, show_id])
    sr_ring_rows = cursor.fetchall()

    cursor.execute("""SELECT n.Number FROM horse_show_number n
        INNER JOIN horse_show_rider r ON n.Rider_id = r.id
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s AND r.Division = "INTERMEDIATE"
        ORDER BY n.Number;""", [class_id, show_id])
    int_ring_rows = cursor.fetchall()

    cursor.execute("""SELECT n.Number FROM horse_show_number n
        INNER JOIN horse_show_rider r ON n.Rider_id = r.id
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s AND r.Division = "JUNIOR"
        ORDER BY n.Number;""", [class_id, show_id])
    jr_ring_rows = cursor.fetchall()

    cursor.execute("""SELECT n.Number, r.FirstName, r.LastName, n.HorseName, r.Division, club.Name
        FROM horse_show_rider r
        INNER JOIN horse_show_club club ON club.id = r.Club_id
        INNER JOIN horse_show_number n ON r.id = n.Rider_id
        INNER JOIN horse_show_entry e ON n.Number = e.Number_id
        INNER JOIN horse_show_classentry ce ON ce.Entry_id = e.id
        INNER JOIN horse_show_showclass c on c.id = ce.ShowClass_id
        WHERE c.id = %s AND e.Show_id = %s
        ORDER BY n.Number;""", [class_id, show_id])
    announce_rows = cursor.fetchall()
    return render(request, 'classes/split_class_print.html', context={'sr_ring':sr_ring_rows, 'int_ring':int_ring_rows,
                                                                    'jr_ring':jr_ring_rows, 'announcer':announce_rows,
                                                                    'cls':sc})

@require_http_methods(["GET"])
def print_rider_sheet(request, show_id, ridernum):
    '''Provides a printable view of class sheets'''
    show = get_object_or_404(Show, pk=show_id)
    number = get_object_or_404(Number, pk=ridernum)
    entries = Entry.objects.filter(Number=number, Show=show)
    if len(entries) == 0:
        return HttpResponse("Rider Number has no Entries")
    classEntries = list(ClassEntry.objects.filter(Entry=entries[0]))
    for clsEntry in classEntries:
        sched = clsEntry.ShowClass.showclassschedule_set.filter(Show=show)
        if len(sched) > 0:
            clsEntry.Position = sched[0].ClassNumber or sched[0].ShowPosition
    return render(request, 'rider_welcome.html', context={'data':{'number':number,
                                                                  'show':show,
                                                                  'classEntries':classEntries}})
    response = HttpResponse()
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize([number], ensure_ascii=False, stream=response)
    return response


#####################################################
##### API ###########################################
#####################################################
@require_http_methods(["GET"])
def api_get_shows(request):
    '''
    Returns a show list in json
    '''
    show_list = Show.objects.all().order_by('-Date')
    json_serializer = serializers.get_serializer("json")()
    response = HttpResponse()
    json_serializer.serialize(show_list, ensure_ascii=False, stream=response)
    return response

@require_http_methods(["GET"])
def api_show(request, show_id):
    #return the show
    json_serializer = serializers.get_serializer("json")()
    json_serializer.serialize(Show.objects.filter(pk=show_id))
    data = json_serializer.getvalue()
    return HttpResponse(data)

@require_http_methods(["POST"])
@staff_member_required
def csv_import(request, show_id):
    #parse csv data
    csvData = csv.DictReader(StringIO.StringIO(request.body))
    show = Show.objects.get(id = show_id)
    (importedEntryType, _) = EntryType.objects.get_or_create(Name="imported")
    data = {"added":[], "failed":[]}
    for row in csvData:
        try:
            # Create/Get the Rider
            riderDivision = Division.objects.get(Division=row["Age division"])
            (rider, created) = Rider.objects.get_or_create(
                FirstName = row["Riders first name"],
                LastName = row["Riders last name"],
                Division = riderDivision,
                Club = Club.objects.get(Name=row["Club"]),
                defaults = {
                    "EmailAddress":row["Contact Email"],
                    "PhoneNumber":row["Contact Phone Number"],
                },
            )
            if created:
                number = Number(
                    Number = row["Riders number"],
                    Rider = rider,
                    HorseName = row["Horses name"]
                )
                number.save()
            else:
                # the rider exists so the number should or we run the risk of cross contaminating
                number = Number.objects.get(Number = row["Riders number"], Rider = rider)
            # now create an entry and assign some class-entries to it
            (entry, _) = Entry.objects.get_or_create(Number = number, Show = show)
            #entry.save()
            #"Showmanship;Saddle Seat Eq;Hunt Seat Eq or English Eq;Discipline Rail English;Bareback Eq"
            for klassName in row["Performance classes"].split(";"):
                klass = ShowClass.objects.get(
                    FormName = klassName,
                    Division = riderDivision,
                )
                (classEntry, _entryAdded) = ClassEntry.objects.get_or_create(Entry = entry, ShowClass = klass, EntryType = importedEntryType)
            # medals
            data["added"].append(row)
        except StrangeError():
            data["failed"].append(row)
    return JsonResponse(data)

class StrangeError(Exception):
    pass
