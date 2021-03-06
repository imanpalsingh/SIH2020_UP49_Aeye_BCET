# Generated by Django 3.0.8 on 2020-08-03 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end_main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='pt_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Patient_name', models.CharField(max_length=100)),
                ('Patient_id', models.CharField(max_length=100)),
                ('HR', models.CharField(max_length=100)),
                ('O2Sat', models.CharField(max_length=100)),
                ('Temp', models.CharField(max_length=100)),
                ('SBP', models.CharField(max_length=100)),
                ('MAP', models.CharField(max_length=100)),
                ('DBP', models.CharField(max_length=100)),
                ('Resp', models.CharField(max_length=100)),
                ('EtCO2', models.CharField(max_length=100)),
                ('BaseExcess', models.CharField(max_length=100)),
                ('HCO3', models.CharField(max_length=100)),
                ('FiO2', models.CharField(max_length=100)),
                ('pH', models.CharField(max_length=100)),
                ('PaCO2', models.CharField(max_length=100)),
                ('SaO2', models.CharField(max_length=100)),
                ('AST', models.CharField(max_length=100)),
                ('BUN', models.CharField(max_length=100)),
                ('Alkalinephos', models.CharField(max_length=100)),
                ('Calcium', models.CharField(max_length=100)),
                ('Chloride', models.CharField(max_length=100)),
                ('Creatinine', models.CharField(max_length=100)),
                ('Bilirubin_direct', models.CharField(max_length=100)),
                ('Glucose', models.CharField(max_length=100)),
                ('Lactate', models.CharField(max_length=100)),
                ('Magnesium', models.CharField(max_length=100)),
                ('Phosphate', models.CharField(max_length=100)),
                ('Potassium', models.CharField(max_length=100)),
                ('Bilirubin_total', models.CharField(max_length=100)),
                ('TroponinI', models.CharField(max_length=100)),
                ('Hct', models.CharField(max_length=100)),
                ('Hgb', models.CharField(max_length=100)),
                ('PTT', models.CharField(max_length=100)),
                ('WBC', models.CharField(max_length=100)),
                ('Fibrinogen', models.CharField(max_length=100)),
                ('Platelets', models.CharField(max_length=100)),
                ('Age', models.CharField(max_length=100)),
                ('Gender', models.CharField(max_length=100)),
                ('HospAdmTime', models.CharField(max_length=100)),
                ('ICULOS', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'pt_data',
            },
        ),
        migrations.DeleteModel(
            name='dbms1',
        ),
    ]
