# Generated by Django 2.1.2 on 2023-05-19 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClassEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='The name of the club', max_length=48, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Danish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=16)),
                ('isMedalsQualifying', models.BooleanField(default=True, verbose_name='Earning this danish qualifies the rider for medals in an appropriate class')),
                ('isStateQualifying', models.BooleanField(default=False, verbose_name='Earning this danish qualifies the rider for State in an appropriate class')),
            ],
            options={
                'verbose_name_plural': 'Danishes',
            },
        ),
        migrations.CreateModel(
            name='Division',
            fields=[
                ('Division', models.CharField(max_length=24, primary_key=True, serialize=False)),
                ('Exclusivity', models.BooleanField(default=True, help_text='Enforces that rider entries MUST match the division when assigned to a class.')),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.CreateModel(
            name='EntryType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='ExtraFee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('Cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('Default', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='FeedBackResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Answer', models.IntegerField()),
                ('FeedBack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.FeedBack')),
                ('FeedBackQuestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.FeedBackQuestion')),
            ],
        ),
        migrations.CreateModel(
            name='HighpointPlacing',
            fields=[
                ('Place', models.IntegerField(primary_key=True, serialize=False)),
                ('Points', models.IntegerField()),
            ],
            options={
                'ordering': ['Place'],
            },
        ),
        migrations.CreateModel(
            name='HighpointTeam',
            fields=[
                ('TeamName', models.CharField(help_text='The name of the Hightpoint Team', max_length=24, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Judge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Judging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Point', models.BooleanField(default=False, help_text="Did the rider 'Point' in the class")),
                ('Comments', models.CharField(blank=True, help_text='What comments did the judge have for the rider', max_length=255, null=True)),
                ('Danish', models.ForeignKey(blank=True, default=None, help_text='What danish did the rider recieve', null=True, on_delete=django.db.models.deletion.CASCADE, to='horse_show.Danish')),
                ('Judge', models.ForeignKey(help_text='Who was the judge for this judging', on_delete=django.db.models.deletion.CASCADE, to='horse_show.Judge')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(help_text='A unique name for this location', max_length=64, unique=True)),
                ('StreetAddress', models.CharField(help_text='The street address for this location', max_length=200)),
                ('City', models.CharField(help_text='The city that this location resides in', max_length=64)),
                ('MailRegion', models.CharField(help_text='The state that this location resides in', max_length=64)),
                ('PostalCode', models.CharField(help_text='The postal code for this locaiton', max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Number',
            fields=[
                ('Number', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('HorseName', models.CharField(max_length=48)),
            ],
        ),
        migrations.CreateModel(
            name='Rider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LastName', models.CharField(max_length=64)),
                ('FirstName', models.CharField(max_length=64)),
                ('MiddleInitial', models.CharField(blank=True, max_length=2, null=True)),
                ('EmailAddress', models.EmailField(blank=True, max_length=254, null=True)),
                ('PhoneNumber', models.CharField(blank=True, max_length=16, null=True)),
                ('Grade', models.CharField(blank=True, max_length=4, null=True)),
                ('Birthday', models.DateField(blank=True, null=True)),
                ('StreetAddress', models.CharField(blank=True, max_length=200, null=True)),
                ('City', models.CharField(blank=True, max_length=64, null=True)),
                ('MailRegion', models.CharField(blank=True, max_length=64, null=True)),
                ('PostalCode', models.CharField(blank=True, max_length=24, null=True)),
                ('Novice', models.BooleanField(default=False)),
                ('Club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Club')),
                ('Division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Division')),
                ('HighpointTeam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.HighpointTeam')),
            ],
        ),
        migrations.CreateModel(
            name='RiderAttributes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Flag', models.CharField(choices=[('NOVICE', 'Novice'), ('OOC', 'Out of County')], help_text='The assigned attribute of this rider', max_length=24)),
                ('Rider', models.ManyToManyField(to='horse_show.Rider')),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=24)),
                ('Style', models.CharField(choices=[('ENGLISH', 'English'), ('WESTERN', 'Western'), ('NONE', 'None')], max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=64, unique=True)),
                ('Description', models.CharField(blank=True, max_length=255, null=True)),
                ('Date', models.DateField(help_text='The date of the show')),
                ('EndDate', models.DateField(help_text='[optional] The date the show ends (if the show is longer then one day)', null=True)),
                ('Location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Location')),
            ],
        ),
        migrations.CreateModel(
            name='ShowClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=48)),
                ('FormName', models.CharField(blank=True, max_length=64, null=True, verbose_name='text to match with entry form')),
                ('isHighpoint', models.BooleanField(default=True, verbose_name='counts toward highpoint')),
                ('isTrail', models.BooleanField(default=False, verbose_name='scored as trail')),
                ('isMedals', models.BooleanField(default=False, verbose_name='scored as medals')),
                ('isMedalsQualifying', models.BooleanField(default=True, verbose_name='qualification for medals')),
                ('isStateQualifying', models.BooleanField(default=False, verbose_name='qualificaiton for state')),
                ('Division', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Division')),
                ('Seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Seat')),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='ShowClassFlags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Flag', models.CharField(choices=[('MEDALSQUAL', 'Qualifies for Medals'), ('STATEQUAL', 'Qualifies for State'), ('TRAIL', 'Score as Trail')], help_text='The name of the flag for this class', max_length=24)),
                ('ShowClass', models.ManyToManyField(to='horse_show.ShowClass')),
            ],
            options={
                'verbose_name': 'Class Flag',
            },
        ),
        migrations.CreateModel(
            name='ShowClassSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShowPosition', models.IntegerField()),
                ('ClassNumber', models.CharField(blank=True, max_length=8, null=True)),
                ('Show', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Show')),
                ('ShowClass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.ShowClass')),
            ],
            options={
                'verbose_name': 'Class Schedule',
                'verbose_name_plural': 'Class Schedules',
                'ordering': ['ShowPosition'],
            },
        ),
        migrations.AddField(
            model_name='number',
            name='HighpointDivision',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Seat'),
        ),
        migrations.AddField(
            model_name='number',
            name='Rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Rider'),
        ),
        migrations.AddField(
            model_name='judging',
            name='Number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Number'),
        ),
        migrations.AddField(
            model_name='judging',
            name='Place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.HighpointPlacing'),
        ),
        migrations.AddField(
            model_name='judging',
            name='SeatRidden',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Seat'),
        ),
        migrations.AddField(
            model_name='judging',
            name='Show',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='horse_show.Show'),
        ),
        migrations.AddField(
            model_name='judging',
            name='ShowClass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.ShowClass'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='Answer',
            field=models.ManyToManyField(through='horse_show.FeedBackResponse', to='horse_show.FeedBackQuestion'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='Rider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Rider'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='Show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Show'),
        ),
        migrations.AddField(
            model_name='entry',
            name='Number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Number'),
        ),
        migrations.AddField(
            model_name='entry',
            name='Show',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Show'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='Entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.Entry'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='EntryType',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='horse_show.EntryType'),
        ),
        migrations.AddField(
            model_name='classentry',
            name='ShowClass',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='horse_show.ShowClass'),
        ),
        migrations.AlterUniqueTogether(
            name='showclassschedule',
            unique_together={('Show', 'ShowPosition')},
        ),
        migrations.AlterOrderWithRespectTo(
            name='number',
            order_with_respect_to='Rider',
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together={('Number', 'Show')},
        ),
    ]