# Generated by Django 2.2 on 2019-12-20 23:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_auto_20190808_1057'),
        ('utility', '0008_auto_20191002_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_id', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('fac_type', models.CharField(choices=[('CC', 'CC'), ('CH', 'CH'), ('CW', 'CW'), ('DS', 'DS'), ('IN', 'IN'), ('PF', 'PF'), ('SS', 'SS'), ('ST', 'ST'), ('TP', 'TP'), ('WL', 'WL'), ('IN', 'IN')], help_text='Type', max_length=2)),
                ('status', models.CharField(choices=[('A', 'A'), ('I', 'I'), ('P', 'P')], max_length=1)),
                ('availability', models.CharField(choices=[('S', 'Seasonal'), ('E', 'Emergency'), ('I', 'Interim'), ('P', 'Permanent'), ('O', 'Other')], max_length=1)),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.CreateModel(
            name='SiteVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=20)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TcrSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tcr_type', models.CharField(choices=[('RT', 'Routine'), ('RP', 'Repeat')], help_text='Type / RP Loc', max_length=2)),
                ('sample_id', models.PositiveIntegerField()),
                ('date', models.DateField()),
                ('sample_point', models.CharField(max_length=10)),
                ('description', models.CharField(help_text='Sample Point Description', max_length=40)),
                ('lab_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='waterutility',
            name='activity_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='waterutility',
            name='principal_city_served',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='waterutility',
            name='principal_county_served',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='waterutility',
            name='system_status',
            field=models.CharField(choices=[('A', 'A')], default='A', max_length=20),
        ),
        migrations.AlterField(
            model_name='assetfinance',
            name='asset_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='waterutility',
            name='primary_water_source_type',
            field=models.CharField(choices=[('GW', 'Ground water'), ('GWP', 'Ground water purchased'), ('SW', 'Surface water'), ('SWP', 'Surface water purchased'), ('GWSW', 'Groundwater under influence of surface water'), ('GWPSW', 'Purchased ground water under influence of surface water')], max_length=5),
        ),
        migrations.AlterField(
            model_name='waterutility',
            name='water_system_type',
            field=models.CharField(choices=[('C', 'Community public water system'), ('NC', 'Noncommunity public water system'), ('TNC', 'Transient, noncommunity public water system'), ('NTNC', 'Nontransient, noncommunity public water system')], max_length=4),
        ),
        migrations.CreateModel(
            name='Violations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('violation_type', models.CharField(choices=[('group', 'Group'), ('individual', 'Individual')], max_length=10)),
                ('fiscal_year', models.PositiveIntegerField(help_text='Federal Fiscal Year for Group Violation')),
                ('violation_id', models.CharField(help_text='Vialation No. for Individual Violation', max_length=10)),
                ('date', models.DateField(help_text='Det. Date')),
                ('type_code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=50)),
                ('analyte_code', models.CharField(help_text='Analyte Group Code / Analyte Code', max_length=40)),
                ('analyte_name', models.CharField(help_text='Analyte Group Name / Analyte Name', max_length=40)),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='TcrSampleSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('requirement_times', models.PositiveIntegerField()),
                ('per_period', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(6)])),
                ('period_unit', models.CharField(choices=[('DL', 'Day'), ('WK', 'Week'), ('MN', 'Month'), ('QT', 'Quater'), ('YR', 'Year')], max_length=2)),
                ('schedule_type', models.CharField(choices=[('routine', 'Routine'), ('repeat', 'Repeat')], help_text='Routine / Repeat', max_length=10)),
                ('original_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.TcrSample')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TcrSampleResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('P', 'P'), ('A', 'A')], max_length=1)),
                ('analyte_name', models.CharField(max_length=40)),
                ('analyte_code', models.CharField(max_length=10)),
                ('method', models.CharField(blank=True, max_length=10)),
                ('mp_date1', models.DateField()),
                ('mp_date2', models.DateField()),
                ('tcr_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.TcrSample')),
            ],
        ),
        migrations.AddField(
            model_name='tcrsample',
            name='water_utility',
            field=models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility'),
        ),
        migrations.CreateModel(
            name='SIteVisitDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(blank=True, max_length=40)),
                ('sev', models.CharField(blank=True, max_length=40)),
                ('desc_code', models.CharField(blank=True, max_length=40)),
                ('desc_text', models.CharField(blank=True, max_length=40)),
                ('freehand_desc', models.CharField(blank=True, max_length=40)),
                ('det_date', models.DateField(null=True)),
                ('res_date', models.DateField(null=True)),
                ('site_visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.SiteVisit')),
            ],
        ),
        migrations.AddField(
            model_name='sitevisit',
            name='water_utility',
            field=models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility'),
        ),
        migrations.CreateModel(
            name='ServiceConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_type', models.CharField(choices=[('RS', 'RS'), ('CM', 'CM'), ('IN', 'IN')], max_length=2)),
                ('count', models.PositiveIntegerField()),
                ('meter_type', models.CharField(choices=[('UM', 'UM'), ('ME', 'ME'), ('MU', 'MU'), ('UN', 'UN')], max_length=2)),
                ('meter_size', models.PositiveIntegerField(default=0, help_text='Meter Size')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('O', 'O'), ('R', 'R'), ('T', 'T'), ('NT', 'NT')], max_length=2)),
                ('name', models.CharField(help_text='Name (e.g. Residential area, Restaurant, Interstate carrier, Highway rest area, etc.)', max_length=50)),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('population', models.PositiveIntegerField(help_text='Population')),
                ('availability', models.CharField(blank=True, choices=[('', 'Blank'), ('S', 'Seasonal'), ('E', 'Emergency'), ('I', 'Interim'), ('P', 'Permanent'), ('O', 'Other')], max_length=1)),
                ('buyer', models.ForeignKey(help_text='Buyer water system', on_delete=django.db.models.deletion.CASCADE, related_name='sale_buyer_sales', to='utility.WaterUtility')),
                ('seller', models.ForeignKey(help_text='Seller water system', on_delete=django.db.models.deletion.CASCADE, related_name='sale_seller_sales', to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='NonTcrSampleSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('requirement_times', models.PositiveIntegerField()),
                ('per_period', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(6)])),
                ('period_unit', models.CharField(choices=[('DL', 'Day'), ('WK', 'Week'), ('MN', 'Month'), ('QT', 'Quater'), ('YR', 'Year')], max_length=2)),
                ('schedule_type', models.CharField(choices=[('group', 'Group'), ('individual', 'Individual')], help_text='Group / Individual', max_length=15)),
                ('init_mp_begin_date', models.DateField(help_text='Init MP Begin Date')),
                ('seasonal', models.CharField(blank=True, max_length=50)),
                ('analyte_code', models.CharField(help_text='Analyte Group Code / Individual Code', max_length=20)),
                ('analyte_name', models.CharField(help_text='Analyte Group Name / Analyte Name', max_length=40)),
                ('facility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utility.Facility')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NonTcrSample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_type', models.CharField(choices=[('PBCU', 'PBCU'), ('primary/secondary', 'Primary / Secondary'), ('SOC', 'SOC'), ('RVOC', 'RVOC')], max_length=20)),
                ('site', models.CharField(max_length=20)),
                ('sample_id', models.CharField(max_length=20)),
                ('date1', models.DateField(help_text='MP Begin Date for PBCU sample, Date for Primary/Secondary, SOC & RVOC sample')),
                ('date2', models.DateField(help_text='MP End Date for PBCU sample, leave as blank for other sample')),
                ('pbcu_type', models.CharField(max_length=10)),
                ('analyte_code', models.CharField(max_length=10)),
                ('analyte_name', models.CharField(max_length=40)),
                ('result', models.CharField(blank=True, help_text='Measure for PBCU sample, Result for other sample', max_length=10)),
                ('unit', models.CharField(blank=True, choices=[('MG/L', 'MG/L')], max_length=10)),
                ('method', models.CharField(blank=True, max_length=50)),
                ('facility', models.ForeignKey(help_text='Facility', on_delete=django.db.models.deletion.CASCADE, to='utility.Facility')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='FacilityProcessDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_process', models.CharField(help_text='Unit Process Name', max_length=50)),
                ('treatment_objective', models.CharField(help_text='Treatment Objective Name', max_length=50)),
                ('treatment_process', models.CharField(help_text='Treatment Process Name', max_length=50)),
                ('facility', models.ForeignKey(help_text='Facility', on_delete=django.db.models.deletion.CASCADE, to='utility.Facility')),
            ],
        ),
        migrations.CreateModel(
            name='FacilityFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver', models.ForeignKey(help_text='Receiving Facility ID', on_delete=django.db.models.deletion.CASCADE, related_name='facilityflow_receiver_flows', to='utility.Facility')),
                ('supplyer', models.ForeignKey(help_text='Supplying Facility ID', on_delete=django.db.models.deletion.CASCADE, related_name='facilityflow_supply_flows', to='utility.Facility')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.AddField(
            model_name='facility',
            name='water_utility',
            field=models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility'),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_type', models.CharField(choices=[('AC', 'Administrative Contact')], max_length=2)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('middle_name', models.CharField(blank=True, max_length=20)),
                ('email1', models.EmailField(blank=True, help_text='First Email', max_length=254)),
                ('email2', models.EmailField(blank=True, help_text='Second Email', max_length=254)),
                ('business_phone1', models.CharField(blank=True, help_text='First Business Phone Number', max_length=20)),
                ('business_phone2', models.CharField(blank=True, help_text='Second Business Phone Number', max_length=20)),
                ('mobile_phone', models.CharField(blank=True, help_text='Mobile Phone Number', max_length=20)),
                ('fax', models.CharField(blank=True, help_text='Facsimile', max_length=20)),
                ('location', models.OneToOneField(help_text='Location / Address', on_delete=django.db.models.deletion.CASCADE, to='geo.Address')),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='CertificationRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Certification Name', max_length=50)),
                ('code', models.CharField(max_length=5)),
                ('begin_date', models.DateField()),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
        migrations.CreateModel(
            name='AnnualOperatingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('begin_date', models.DateField(help_text='Eff. Begin Date', null=True)),
                ('end_date', models.DateField(help_text='Eff. End Date', null=True)),
                ('start_month_day', models.CharField(default='1/1', help_text='Start Month/Day', max_length=5)),
                ('end_month_day', models.CharField(default='12/31', help_text='End Month/Day', max_length=5)),
                ('operating_type', models.CharField(choices=[('R', 'R'), ('T', 'T'), ('NT', 'NT')], max_length=5)),
                ('water_utility', models.ForeignKey(help_text='Water Utility', on_delete=django.db.models.deletion.CASCADE, to='utility.WaterUtility')),
            ],
        ),
    ]
