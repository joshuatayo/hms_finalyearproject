# Generated by Django 3.1.7 on 2021-05-07 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_druginventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='DrugPrescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.drug', verbose_name='Drug')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.IntegerField()),
                ('firstname', models.CharField(max_length=255)),
                ('middlename', models.CharField(blank=True, max_length=255, null=True)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('dob', models.DateField()),
                ('marital_status', models.CharField(choices=[('', '- Marital Status -'), ('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], max_length=20)),
                ('gender', models.CharField(choices=[('', '- Gender -'), ('Male', 'Male'), ('Female', 'Female')], max_length=10)),
                ('address', models.TextField(blank=True, null=True)),
                ('city_town', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
        migrations.CreateModel(
            name='PatientTreatment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('complaint', models.TextField(blank=True, null=True)),
                ('diagnosis', models.TextField(blank=True, null=True)),
                ('recommend', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient', verbose_name='Patient')),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(blank=True, max_length=255, null=True)),
                ('fullname', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_no', models.CharField(blank=True, max_length=255, null=True)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('method', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patienttreatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patienttreatment', verbose_name='PatientTreatment')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
        migrations.CreateModel(
            name='PatientTreatmentStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('patienttreatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patienttreatment', verbose_name='PatientTreatment')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
        migrations.CreateModel(
            name='DrugPrescriptionStaff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('drugprescription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.drugprescription', verbose_name='DrugPrescription')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
        migrations.AddField(
            model_name='drugprescription',
            name='patienttreatment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patienttreatment', verbose_name='PatientTreatment'),
        ),
        migrations.CreateModel(
            name='CardPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('card_id', models.IntegerField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.patient', verbose_name='Patient')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient', verbose_name='Patient')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Staff')),
            ],
        ),
    ]
