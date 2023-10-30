# Generated by Django 4.2.6 on 2023-10-29 18:51

import autoslug.fields
import datetime
import dirtyfields.dirtyfields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Hospital', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='get_full_name', unique=True)),
                ('department', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('degrees', models.CharField(max_length=255)),
                ('medical_school', models.CharField(max_length=255)),
                ('license_number', models.CharField(max_length=50)),
                ('license_expiry_date', models.DateField()),
                ('emergency_contact', models.CharField(max_length=15)),
                ('languages_spoken', models.TextField()),
                ('notes', models.TextField(blank=True)),
                ('doctor_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DoctorSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_time', models.TimeField(default=datetime.time(9, 0))),
                ('end_time', models.TimeField(default=datetime.time(17, 0))),
                ('activity_type', models.CharField(choices=[('patient_exam', 'Patient Examination'), ('surgery', 'Surgery'), ('testing_lab', 'Testing Lab')], default='patient_exam', max_length=20)),
                ('maximum_patient', models.IntegerField()),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('hospital', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hospital.hospital')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EmergencyDoctorScedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('schedule_date', models.DateField(blank=True)),
                ('doctor_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctorschedule')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DoctorScheduleDaysConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Common.days')),
                ('doctor_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctorschedule')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
        migrations.CreateModel(
            name='DoctorSpecialtyConnector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.doctor')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Common.specialty')),
            ],
            options={
                'ordering': ('-created_at',),
                'unique_together': {('doctor', 'specialty')},
            },
            bases=(dirtyfields.dirtyfields.DirtyFieldsMixin, models.Model),
        ),
    ]
