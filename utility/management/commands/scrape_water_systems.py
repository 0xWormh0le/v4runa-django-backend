from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from scrapy.crawler import CrawlerProcess
import re
import logging
import scrapy
import zipcodes
from math import floor
from datetime import datetime

from geo.models import Address
from utility.models import (
    WaterUtility,
    Contact,
    AnnualOperatingPeriod,
    ServiceConnection,
    ServiceArea,
    CertificationRequirement,
    Facility,
    FacilityProcessDetail,
    FacilityFlow,
    Sale,
    TcrSample,
    TcrSampleSchedule,
    TcrSampleResult,
    NonTcrSample,
    NonTcrSampleSchedule,
    Violation,
    SiteVisit,
    SiteVisitDetail
)


base_selector = 'body>table>tr>td>'
summary_selector = (
    base_selector + 'table:nth-child(1)>tr:nth-child(n+1)>td:nth-child({})>p'
)
contact_selector = (
    base_selector + 'table:nth-child(2)>tr:nth-child(3)>td:nth-child({})'
)
annual_operating_period_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(1)>tr:nth-child(n+3)>td:nth-child({})'
)
service_connection_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(2)>tr:nth-child(n+3)>td:nth-child({})'
)
service_area_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(3)>tr:nth-child(n+3)>td:nth-child({})'
)
certification_requirement_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(4)>tr:nth-child(n+3)>td:nth-child({})'
)
facility_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(5)>tr:nth-child(n+3)>td:nth-child({})>font'
)
facility_flow_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(6)>tr:nth-child(n+3)>td:nth-child({})>font'
)
buy_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(8)>tr:nth-child(n+3)>td>a'
)
routine_tcr_schedule_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(9)>tr:nth-child(n+3)>td:nth-child({})>font'
)
repeat_tcr_schedule_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(10)>tr:nth-child(n+3)>td:nth-child({})>font'
)
group_non_tcr_schedule_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(11)>tr:nth-child(n+3)>td:nth-child({})>font'
)
individual_non_tcr_schedule_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(12)>tr:nth-child(n+3)>td:nth-child({})>font'
)
group_violation_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(13)>tr:nth-child(n+3)>td:nth-child({})>font'
)
individual_violation_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(14)>tr:nth-child(n+3)>td:nth-child({})>font'
)
tcr_sample_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(15)>tr:nth-child(n+3)>td:nth-child({})>font'
)
pbcu_sample_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(16)>tr:nth-child(n+3)>td:nth-child({})>font'
)
site_visit_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(17)>tr:nth-child(n+3)>td:nth-child({})>font'
)
ps_sample_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(18)>tr:nth-child(n+3)>td:nth-child({})>font'
)

soc_sample_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(19)>tr:nth-child(n+3)>td:nth-child({})>font'
)

rvoc_sample_result_selector = (
    base_selector + 'table:nth-child(2)>table:nth-of-type(20)>tr:nth-child(n+3)>td:nth-child({})>font'
)


def eat_spaces(str):
    str = re.sub('\xa0|\t', ' ', str)
    str = re.sub('\r|\n', '', str)
    str = re.sub(' +', ' ', str)
    return str.lstrip().rstrip()

def format_date(date):
    return datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')

def dom_text(response, selector, title = True, raw = False, single = False):
    texts = []
    doms = response.css(selector).getall()

    for x in doms:
        start = x.find('>') + 1
        end = x.rfind('<')
        text = x[start:end]

        if not raw:
            text = eat_spaces(text)
            if title:
                text = text.title()

        texts.append(text)

    if single:
        if len(texts) > 0:
            return texts[0]
        else:
            return None
    else:
        return texts


def destructure_requirement(requirement):
    requirement_times, _, period_unit = re.split(' |/', requirement)
    per_period = 1

    if period_unit[0].isdigit():
        per_period = period_unit[0]
        period_unit = period_unit[1:]

    if period_unit == 'Y':
        period_unit = 'YR'
    
    return {
        'requirement_times': requirement_times,
        'per_period': per_period,
        'period_unit': period_unit
    }


def create_location(response):
    selector = contact_selector.format(2)
    contact_field = dom_text(response, selector, raw=True, single=True)
    contact_field = contact_field.split('<br>')
    
    street = eat_spaces(contact_field[1]).title()
    region = re.split(',|\xa0', contact_field[-1])
    city = eat_spaces(region[0]).title()
    state = eat_spaces(region[-2])
    zip_code = eat_spaces(region[-1])

    longitude, latitude = (0, 0)
    
    try:
        location = zipcodes.matching(zip_code)
        longitude = location[0]['lat']
        latitude = location[0]['long']
    except:
        pass

    water_system_location = Address(
        street_address_1=street,
        city=city,
        state=state,
        country=state,
        zip_code=zip_code,
        longitude=longitude,
        latitude=latitude
    )

    contact_location = Address(
        street_address_1=street,
        city=city,
        state=state,
        country=state,
        zip_code=zip_code,
        longitude=longitude,
        latitude=latitude
    )
    
    water_system_location.save()
    contact_location.save()

    return (water_system_location, contact_location)


def create_water_utility(response, location):
    water_system_id, name, principal_county_served, principal_city_served = (
        dom_text(response, summary_selector.format(2))
    )
    water_system_type, primary_water_source_type, system_status, activity_date = (
        dom_text(response, summary_selector.format(4), title=False)
    )
    name_font = dom_text(
        response,
        base_selector + 'table:nth-child(1)>tr:nth-child(3)>td:nth-child(2)>p>font',
        single=True
    )

    water_system_id = water_system_id.upper()
    activity_date = format_date(activity_date)

    if name_font is not None:
        name = name_font

    population = dom_text(response, annual_operating_period_selector.format(6))
    population_sum = 0

    for p in population:
        p = eat_spaces(p)
        if p: population_sum += int(p)

    try:
        water_utility = WaterUtility.objects.get(water_system_id=water_system_id)
    except ObjectDoesNotExist:
        water_utility = WaterUtility(water_system_id=water_system_id)

    water_utility.name = name
    water_utility.water_system_type = water_system_type
    water_utility.population = population_sum
    water_utility.principal_county_served = principal_county_served
    water_utility.principal_city_served = principal_city_served
    water_utility.primary_water_source_type = primary_water_source_type
    water_utility.system_status = system_status
    water_utility.activity_date = activity_date
    water_utility.location = location
    water_utility.url = response.url
    water_utility.save()
    
    return water_utility


def create_contact(response, water_utility, location):
    contact_type = dom_text(response, contact_selector.format(1), single=True)
    contact_type = contact_type.split('-')[0].upper()
    
    contact_field = dom_text(response, contact_selector.format(2), single=True, raw=True)
    name = contact_field.split('<br>')[0].split(',')
    first_name = eat_spaces(name[0]).title()
    last_name = eat_spaces(name[1]).title()
    middle_name = eat_spaces(name[2]).title() if len(name) > 2 else None

    try:
        contact = Contact.objects.get(water_utility=water_utility)
    except ObjectDoesNotExist:
        contact = Contact(water_utility=water_utility)

    contact.contact_type = contact_type
    contact.first_name = first_name
    contact.last_name = last_name
    contact.middle_name = middle_name
    contact.location = location

    contact_communication_selector = contact_selector.format(3) + '>table>tr:not(:first-child)>td'
    contacts = dom_text(response, contact_communication_selector, title=False)
    email_count = 0
    bus_count = 0

    for tp, value in zip(contacts, contacts[1:]):
        value = eat_spaces(value)
        if len(value) > 0:
            if tp[0:5] == 'EMAIL':
                if email_count == 0:
                    contact.email1 = value
                else:
                    contact.email2 = value
                email_count += 1
            elif tp[0:3] == 'BUS':
                if bus_count == 0:
                    contact.business_phone1 = value
                else:
                    contact.business_phone2 = value
                bus_count += 1
            elif tp[0:3] == 'MOB':
                contact.mobile_phone = value
            elif tp[0:3] == 'FAX':
                contact.fax = value

    contact.save()
    return contact


def create_annual_operating_period(response, water_utility):
    begin_dates = dom_text(response, annual_operating_period_selector.format(1))
    end_dates = dom_text(response, annual_operating_period_selector.format(2))
    start_month_days = dom_text(response, annual_operating_period_selector.format(3))
    end_month_days = dom_text(response, annual_operating_period_selector.format(4))
    operating_types = dom_text(response, annual_operating_period_selector.format(5), title=False)
    populations = dom_text(response, annual_operating_period_selector.format(6))

    for i in range(len(begin_dates)):
        end_date = None

        if end_dates[i] != 'No End Date':
            end_date = format_date(end_dates[i])

        annual_operating_period = AnnualOperatingPeriod(
            water_utility=water_utility,
            begin_date=format_date(begin_dates[i]),
            end_date=end_date,
            start_month_day=start_month_days[i],
            end_month_day=end_month_days[i],
            operating_type=operating_types[i],
            population=populations[i]
        )

        annual_operating_period.save()

    return True


def create_service_connection(response, water_utility):
    connection_types = dom_text(response, service_connection_selector.format(1), title=False)
    counts = dom_text(response, service_connection_selector.format(2))
    meter_types = dom_text(response, service_connection_selector.format(3), title=False)
    meter_sizes = dom_text(response, service_connection_selector.format(4))

    for i in range(len(connection_types)):
        service_connection = ServiceConnection(
            water_utility=water_utility,
            connection_type=connection_types[i],
            count=counts[i],
            meter_type=meter_types[i],
            meter_size=meter_sizes[i]
        )
        service_connection.save()

    return True


def create_service_area(response, water_utility):
    codes = dom_text(response, service_area_selector.format(1), title=False)
    names = dom_text(response, service_area_selector.format(2))

    for i in range(len(codes)):
        service_connection = ServiceArea(
            water_utility=water_utility,
            code=codes[i],
            name=names[i]
        )
        service_connection.save()

    return True


def create_certification_requirement(response, water_utility):
    names = dom_text(response, certification_requirement_selector.format(1))
    codes = dom_text(response, certification_requirement_selector.format(2), title=False)
    begin_dates = dom_text(response, certification_requirement_selector.format(3))

    for i in range(len(names)):
        service_connection = CertificationRequirement(
            water_utility=water_utility,
            name=names[i],
            code=codes[i]
        )

        if begin_date and begin_date != 'No Begin Date':
            service_connection.begin_date = format_date(begin_dates[i])
        
        service_connection.save()

    return True


def create_facility(response, water_utility):
    facility_ids = dom_text(response, facility_selector.format(1) + '>a', title=False)
    names = dom_text(response, facility_selector.format(2))
    fac_statuses = dom_text(response, facility_selector.format(3), title=False)
    processes = dom_text(response, facility_selector.format(4))

    for i in range(len(facility_ids)):
        fac_type, status, availability = fac_statuses[i].split('-')
        facility = Facility(
            water_utility=water_utility,
            facility_id=facility_ids[i],
            name=names[i],
            fac_type=eat_spaces(fac_type),
            status=eat_spaces(status),
            availability=eat_spaces(availability)
        )
        facility.save()

        facility_process_selector = base_selector + 'table:nth-child(2)>table:nth-of-type(5)>tr:nth-child({})>td:nth-child(4)>font>table>tr>td:nth-child({})>font'
        unit_processes = dom_text(response, facility_process_selector.format(i + 3, 1))
        treatment_objectives = dom_text(response, facility_process_selector.format(i + 3, 2))
        treatment_processes = dom_text(response, facility_process_selector.format(i + 3, 3))

        for j in range(len(unit_processes)):
            process_detail = FacilityProcessDetail(
                facility=facility,
                unit_process=unit_processes[j],
                treatment_objective=treatment_objectives[j],
                treatment_process=treatment_processes[j]
            )
            process_detail.save()

    return True


def create_facility_flow(response, water_utility):
    suppliers = dom_text(response, facility_flow_selector.format(1), title=False)
    receivers = dom_text(response, facility_flow_selector.format(3), title=False)

    for i in range(len(suppliers)):
        supplier = eat_spaces(suppliers[i].split('-')[1])
        receiver = eat_spaces(receivers[i].split('-')[1])

        try:
            facility_flow = FacilityFlow(
                water_utility=water_utility,
                supplier=Facility.objects.get(facility_id=supplier),
                receiver=Facility.objects.get(facility_id=receiver)
            )
            facility_flow.save()
        except:
            pass

    return True


def create_water_sale(response, water_utility):
    buys = dom_text(response, buy_selector, title=False)

    for i in range(len(buys)):
        try:
            buyer = WaterUtility.objects.get(water_system_id=buys[i])
        except:
            continue

        try:
            sale = Sale.objects.get(seller=water_utility, buyer=buyer)
        except:
            sale = Sale(seller=water_utility, buyer=buyer)

        selector = base_selector + 'table:nth-child(2)>table:nth-of-type(8)>tr:nth-child({})>td'
        text = dom_text(response, selector.format(i + 3), title=False, single=True)
        start = text.find('</a>') + 4
        end = text.find('<br>')
        _, population, availability = text[start:end].split('/')
        sale.population = eat_spaces(population.replace('&amp;nbsp', ''))
        sale.availability = eat_spaces(availability.replace('&amp;nbsp', ''))
        sale.save()
    
    return True


def create_routine_tcr_schedule(response, water_utility):
    begin_dates = dom_text(response, routine_tcr_schedule_selector.format(1))
    end_dates = dom_text(response, routine_tcr_schedule_selector.format(2))
    requirements = dom_text(response, routine_tcr_schedule_selector.format(3), title=False)

    for i in range(len(begin_dates)):
        requirement = destructure_requirement(requirements[i])
        end_date = None

        if end_dates[i] and end_dates[i] != 'Continuous':
            end_date = format_date(end_dates[i])

        tcr_sample_schedule = TcrSampleSchedule(
            water_utility=water_utility,
            schedule_type='routine',
            begin_date=format_date(begin_dates[i]),
            end_date=end_date,
            requirement_times=requirement['requirement_times'],
            per_period=requirement['per_period'],
            period_unit=requirement['period_unit']
        )

        tcr_sample_schedule.save()
    
    return True


def create_repeat_tcr_schedule(response, water_utility):
    begin_dates = dom_text(response, repeat_tcr_schedule_selector.format(1))
    end_dates = dom_text(response, repeat_tcr_schedule_selector.format(2))
    requirements = dom_text(response, repeat_tcr_schedule_selector.format(3), title=False)
    original_samples = dom_text(response, repeat_tcr_schedule_selector.format(4))

    if len(begin_dates) == 1 and len(end_dates) == 0:
        return False
    
    for i in range(len(begin_dates)):
        requirement = destructure_requirement(requirements[i])
        end_date = None

        if end_dates[i] and end_dates[i] != 'Continuous':
            end_date = format_date(end_dates[i])

        tcr_sample_schedule = TcrSampleSchedule(
            water_utility=water_utility,
            schedule_type='repeat',
            begin_date=format_date(begin_dates[i]),
            end_date=end_date,
            requirement_times=requirement['requirement_times'],
            per_period=requirement['per_period'],
            period_unit=requirement['period_unit']
        )

        if original_samples[i]:
            try:
                original_sample = eat_spaces(original_samples[i].split('/')[0])
                tcr_sample_schedule.original_sample = TcrSample.objects.get(sample_id=original_sample)
            except:
                pass

        tcr_sample_schedule.save()
    
    return True


def create_group_non_tcr_schedule(response, water_utility):
    facilities = dom_text(response, group_non_tcr_schedule_selector.format(1) + '>a', title=False)
    begin_dates = dom_text(response, group_non_tcr_schedule_selector.format(2))
    end_dates = dom_text(response, group_non_tcr_schedule_selector.format(3))
    requirements = dom_text(response, group_non_tcr_schedule_selector.format(4), title=False)
    analyte_codes = dom_text(response, group_non_tcr_schedule_selector.format(5), title=False)
    analyte_names = dom_text(response, group_non_tcr_schedule_selector.format(6))

    for i in range(len(facilities)):
        requirement = destructure_requirement(requirements[i])
        end_date = None

        if end_dates[i] and end_dates[i] != 'Continuous':
            end_date = format_date(end_dates[i])

        try:
            non_tcr_sample_schedule = NonTcrSampleSchedule(
                water_utility=water_utility,
                schedule_type='group',
                facility=Facility.objects.get(facility_id=facilities[i]),
                begin_date=format_date(begin_dates[i]),
                end_date=end_date,
                requirement_times=requirement['requirement_times'],
                per_period=requirement['per_period'],
                period_unit=requirement['period_unit'],
                analyte_code=analyte_codes[i],
                analyte_name=analyte_names[i]
            )
            non_tcr_sample_schedule.save()
        except:
            pass

    return True


def create_individual_non_tcr_schedule(response, water_utility):
    facilities = dom_text(response, individual_non_tcr_schedule_selector.format(1) + '>a', title=False)
    begin_end_dates = dom_text(response, individual_non_tcr_schedule_selector.format(2), raw=True)
    init_mp_begin_dates = dom_text(response, individual_non_tcr_schedule_selector.format(3))
    seasonals = dom_text(response, individual_non_tcr_schedule_selector.format(4))
    requirements = dom_text(response, individual_non_tcr_schedule_selector.format(5), title=False)
    analyte_codes = dom_text(response, individual_non_tcr_schedule_selector.format(6)[:-5])
    analyte_names = dom_text(response, individual_non_tcr_schedule_selector.format(7))

    for i in range(len(facilities)):
        requirement = destructure_requirement(requirements[i])
        begin_date, end_date = re.split('\t  |<br>', begin_end_dates[i])
        begin_date = eat_spaces(begin_date)
        end_date = eat_spaces(end_date)

        if end_date and end_date != 'Continuous':
            end_date = format_date(end_date)
        else:
            end_date = None

        try:
            non_tcr_sample_schedule = NonTcrSampleSchedule(
                water_utility=water_utility,
                schedule_type='individual',
                facility=Facility.objects.get(facility_id=facilities[i]),
                begin_date=format_date(begin_date),
                end_date=end_date,
                init_mp_begin_date=format_date(init_mp_begin_dates[i]),
                seasonal=seasonals[i],
                requirement_times=requirement['requirement_times'],
                per_period=requirement['per_period'],
                period_unit=requirement['period_unit'],
                analyte_code=analyte_codes[i],
                analyte_name=analyte_names[i]
            )
            non_tcr_sample_schedule.save()
        except:
            pass

    return True


def create_violation(response, water_utility):
    selectors = (group_violation_selector, individual_violation_selector)
    violation_types = ('group', 'individual')

    for selector_key, selector in enumerate(selectors):
        id_years = dom_text(response, selector.format(1) + '>a')
        dates = dom_text(response, selector.format(2))
        type_codes = dom_text(response, selector.format(3), title=False)
        names = dom_text(response, selector.format(4))
        analyte_codes = dom_text(response, selector.format(5), title=False)
        analyte_names = dom_text(response, selector.format(6))

        if len(id_years) == 1 and len(dates) == 0:
            continue
        
        for i in range(len(id_years)):
            violation = Violation(
                water_utility=water_utility,
                violation_type=violation_types[selector_key],
                date=format_date(dates[i]),
                type_code=type_codes[i],
                name=names[i],
                analyte_code=analyte_codes[i],
                analyte_name=analyte_names[i]
            )

            if selector_key == 0:
                fiscal_year = id_years[i]
            else:
                fiscal_year, violation_id = id_years[i].split('-')
                violation.violation_id = violation_id

            violation.fiscal_year = fiscal_year
            violation.save()

    return True


def create_tcr_sample(response, water_utility):
    type_locs = dom_text(response, tcr_sample_result_selector.format(1), title=False)
    sample_ids = dom_text(response, tcr_sample_result_selector.format(2) + '>a', title=False)
    dates = dom_text(response, tcr_sample_result_selector.format(3))
    sample_points = dom_text(response, tcr_sample_result_selector.format(4), title=False)
    descriptions = dom_text(response, tcr_sample_result_selector.format(5))
    lab_ids = dom_text(response, tcr_sample_result_selector.format(6), title=False)
    
    for i in range(len(type_locs)):
        tcr_type, rp_loc = type_locs[i].split('<br>')
        sample_id = sample_ids[i].split('<br>')[0]
        tcr_sample = TcrSample(
            water_utility=water_utility,
            tcr_type=eat_spaces(tcr_type),
            sample_id=eat_spaces(sample_id),
            date=format_date(dates[i]),
            sample_point=sample_points[i],
            description=descriptions[i],
            lab_id=lab_ids[i]
        )

        rp_loc = eat_spaces(rp_loc)
        if rp_loc:
            tcr_sample.rp_loc = rp_loc

        result_summary_selector = 'table:nth-child(2)>table:nth-of-type(15)>tr:nth-child({})>td:nth-child(7)>font'
        result_summary = dom_text(response, result_summary_selector.format(i + 3), single=True)
        if result_summary:
            tcr_sample.result_summary = result_summary

        tcr_sample.save()

        result_detail_selector = 'table:nth-child(2)>table:nth-of-type(15)>tr:nth-child({})>td:nth-child(7)>table>tr>td:nth-child({})>font'
        results = dom_text(response, result_detail_selector.format(i + 3, 1), title=False)
        analytes = dom_text(response, result_detail_selector.format(i + 3, 2), title=False)
        methods = dom_text(response, result_detail_selector.format(i + 3, 3), title=False)
        mp_dates = dom_text(response, result_detail_selector.format(i + 3, 4), title=False)

        for j in range(len(results)):
            analyte_code_start = analytes[j].rfind('(')
            analyte_name = eat_spaces(analytes[j][:analyte_code_start - 1])
            analyte_code = eat_spaces(analytes[j][analyte_code_start + 1:-1])
            mp_date = mp_dates[j]

            tcr_sample_result = TcrSampleResult(
                tcr_sample=tcr_sample,
                result=results[j],
                analyte_name=analyte_name,
                analyte_code=analyte_code
            )

            if methods[j]:
                tcr_sample_result.method = methods[j]

            if mp_date:
                mp_date = mp_date.split('<br>')

                if len(mp_date) > 1:
                    mp_date1 = eat_spaces(mp_date[0])
                    mp_date2 = eat_spaces(mp_date[1])
                    if mp_date1:
                        tcr_sample_result.mp_date1 = format_date(mp_date1)
                    if mp_date2:
                        tcr_sample_result.mp_date2 = format_date(mp_date2)
                else:
                    tcr_sample_result.mp_date1 = format_date(mp_date[0])

            tcr_sample_result.save()

    return True


def create_pbcu_sample(response, water_utility):
    begin_dates = dom_text(response, pbcu_sample_result_selector.format(1), title=False)
    pbcu_types = dom_text(response, pbcu_sample_result_selector.format(2), title=False)
    sample_ids = dom_text(response, pbcu_sample_result_selector.format(3) + ':last-child')
    results = dom_text(response, pbcu_sample_result_selector.format(4))
    units = dom_text(response, pbcu_sample_result_selector.format(5), title=False)
    analytes = dom_text(response, pbcu_sample_result_selector.format(6))

    for i in range(len(begin_dates)):
        start = begin_dates[i].find('"Samples in Summary">')
        begin_date = begin_dates[i][start:]
        date1, date2 = begin_date.split('<br>')
        start = date1.find('>') + 1
        end = date1.rfind('</')
        date1 = date1[start:end]
        date2 = eat_spaces(date2)

        analyte_code, analyte_name = analytes[i].split('-')

        non_tcr_sample = NonTcrSample(
            water_utility=water_utility,
            date1=format_date(date1),
            date2=format_date(date2),
            sample_id=sample_ids[i],
            sample_type='PBCU',
            pbcu_type=pbcu_types[i],
            analyte_code=eat_spaces(analyte_code).upper(),
            analyte_name=eat_spaces(analyte_name)
        )

        if results[i]:
            non_tcr_sample.result = results[i]

        if units[i]:
            non_tcr_sample.unit = units[i]

        non_tcr_sample.save()

    return True


def create_site_visit(response, water_utility):
    reasons = dom_text(response, site_visit_result_selector.format(1) + '>a', title=False)
    dates = dom_text(response, site_visit_result_selector.format(2))

    for i in range(len(reasons)):
        site_visit = SiteVisit(
            water_utility=water_utility,
            reason=reasons[i],
            date=format_date(dates[i])
        )

        site_visit.save()

        visit_detail_selector = 'table:nth-child(2)>table:nth-of-type(17)>tr:nth-child({})>td:nth-child(3)>table>tr>td:nth-child({})>font'

        cats = dom_text(response, visit_detail_selector.format(i + 3, 1))
        sevs = dom_text(response, visit_detail_selector.format(i + 3, 2))
        descs = dom_text(response, visit_detail_selector.format(i + 3, 3), title=False)
        freehand_descs = dom_text(response, visit_detail_selector.format(i + 3, 4))
        det_dates = dom_text(response, visit_detail_selector.format(i + 3, 5))
        res_dates = dom_text(response, visit_detail_selector.format(i + 3, 6))

        if len(cats) == 1 and len(sevs) == 0:
            continue
        
        for j in range(len(cats)):
            site_visit_detail = SiteVisitDetail(
                site_visit=site_visit,
                cat=cats[j],
                sev=sevs[j]
            )

            desc = descs[j].split('<br>')
            desc_code = eat_spaces(desc[0])

            if desc_code:
                site_visit_detail.desc_code = desc_code
                
            if len(desc) > 1:
                desc_text = eat_spaces(desc[1]).title()
                if desc_text:
                    site_visit_detail.desc_text = desc_text

            if freehand_descs[j]:
                site_visit_detail.freehand_desc = freehand_descs[j]

            if det_dates[j]:
                site_visit_detail.det_date = format_date(det_dates[j])

            if res_dates[j]:
                site_visit_detail.res_date = format_date(res_dates[j])
            
            site_visit_detail.save()

    return True


def create_non_tcr_sample(response, water_utility):
    selectors = (
        ps_sample_result_selector,
        soc_sample_result_selector,
        rvoc_sample_result_selector
    )

    sample_types = ('primary/secondary', 'SOC', 'RVOC')

    for selector_key, selector in enumerate(selectors):
        fac_sites = dom_text(response, selector.format(1), title=False)
        sample_ids = dom_text(response, selector.format(2), title=False)
        dates = dom_text(response, selector.format(3))
        analyte_codes = dom_text(response, selector.format(4), title=False)
        analyte_names = dom_text(response, selector.format(5))
        results = dom_text(response, selector.format(6), title=False)
        units = dom_text(response, selector.format(7), title=False)
        methods = dom_text(response, selector.format(8), title=False)

        for i in range(len(fac_sites)):
            fac_site = fac_sites[i]
            start = fac_site.find('-')
            facility_id = fac_site[:start]
            site = fac_site[start + 1:]

            try:
                non_tcr_sample = NonTcrSample(
                    water_utility=water_utility,
                    sample_type=sample_types[selector_key],
                    facility=Facility.objects.get(facility_id=facility_id),
                    site=site,
                    sample_id=sample_ids[i],
                    date1=format_date(dates[i]),
                    analyte_code=analyte_codes[i],
                    analyte_name=analyte_names[i],
                    result=results[i],
                    method=methods[i]
                )

                if units[i]:
                    start = units[i].find('>') + 1
                    end = units[i].rfind('<')
                    unit = units[i][start:end]
                    if unit:
                        non_tcr_sample.unit = unit

                non_tcr_sample.save()
            except:
                pass

    return True


class WaterSystemSpider(scrapy.Spider):
    name = 'water system'
    base_url = 'https://dww2.tceq.texas.gov/DWW//JSP/'
    search_url = 'SearchDispatch?number=&name=&ActivityStatusCD=A&county=All&WaterSystemType=All&SourceWaterType=All&SampleType=null&begin_date=12%2F17%2F2018&end_date=12%2F17%2F2019&action=Search+For+Water+Systems'
    progress_length = 50
    funcs = (
        create_annual_operating_period,
        create_service_connection,
        create_service_area,
        create_certification_requirement,
        create_facility,
        create_facility_flow,
        create_routine_tcr_schedule,        
        create_group_non_tcr_schedule,        
        create_individual_non_tcr_schedule,
        create_violation,
        create_tcr_sample,
        create_pbcu_sample,
        create_site_visit,
        create_non_tcr_sample,
        create_repeat_tcr_schedule
    )


    def show_progress(self):
        done_count = round(self.progress_length * self.progress / self.total)
        progress = '#' * done_count + ' ' * (self.progress_length - done_count)
        percent = '{:.3f}'.format(round(100 * self.progress / self.total, 3))
        print('\r    [{}] {}% ({} / {})'.format(progress, percent, floor(self.progress), self.total), end='', flush=True)


    def start_requests(self):
        print('[1/4] Requesting Base URL')
        url = self.base_url + self.search_url
        yield scrapy.Request(url=url, callback=self.parse_base_url)


    def parse_base_url(self, response):
        print('[2/4] Working on DOM for fact sheet links')
        self.fact_sheet_links = response.css('table table tr:not(:first-child) td:nth-child(2)>a::attr(href)').getall()

        print('[3/4] Creating Water Systems')
        self.total = len(self.fact_sheet_links)
        self.progress = 0
        self.done = 0

        for link in self.fact_sheet_links:
            url = self.base_url + link
            yield scrapy.Request(url=url, callback=self.handle_fact_sheet)


    def handle_fact_sheet(self, response):
        self.work_fact_sheet(response)
        self.done += 1

        if self.done == self.total:
            self.progress = 0
            self.done = 0

            print('')
            print('[4/4] Building sales for per water system')

            for link in self.fact_sheet_links:
                url = self.base_url + link
                yield scrapy.Request(url=url, callback=self.handle_water_sale, dont_filter=True)


    def handle_water_sale(self, response):
        self.work_water_sale(response)
        self.done += 1
        if self.done == self.total:
            print('')
            print('Completed')


    def work_fact_sheet(self, response):
        self.show_progress()

        step = 1 / 18
        water_system_location, contact_location = create_location(response)
        self.progress += step
        self.show_progress()
        
        water_utility = create_water_utility(response, water_system_location)
        self.progress += step
        self.show_progress()

        create_contact(response, water_utility, contact_location)
        self.progress += step
        self.show_progress()

        for func in self.funcs:
            func(response, water_utility)
            self.progress += step
            self.show_progress()

        self.progress = self.done + 1
        self.show_progress()
        
        
    def work_water_sale(self, response):
        self.show_progress()
        water_system_id = dom_text(response, summary_selector.format(2), single=True)
        water_system_id = water_system_id.upper()
        
        try:
            water_utility = WaterUtility.objects.get(water_system_id=water_system_id)
            create_water_sale(response, water_utility)
        except:
            pass

        self.progress += 1
        self.show_progress()


class Command(BaseCommand):
    help = ('Fill databases with scrapped data from water system pages')

    def handle(self, *args, **options):
        logging.getLogger('scrapy').propagate = False
        process = CrawlerProcess()
        process.crawl(WaterSystemSpider)
        process.start()
