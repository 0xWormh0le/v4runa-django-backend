import json
from .models import TempReport


def import_temp_report_from_json(json_file, user):
    json_reports = json.load(json_file)
    temp_reports = []
    for report in json_reports:
        if type(report['qualityTable']) == list:
            if len(report['qualityTable']) > 0:
                quality_table = report['qualityTable'][0]
                quality_table_new = {}
                for key in quality_table:
                    if type(quality_table[key]) is list:
                        if len(quality_table[key]) > 0:
                            subquality = quality_table[key][0]
                            subquality_new = {}
                            for chemical in subquality:
                                if len(subquality[chemical]) > 0 and type(subquality[chemical]) is list:
                                    subquality_new[chemical] = subquality[chemical][0]
                                else:
                                    subquality_new[chemical] = subquality[chemical]
                            quality_table_new[key] = subquality_new
                        else:
                            pass
                    else:
                        quality_table_new[key] = quality_table[key]
                report['qualityTable'] = quality_table_new
            else:
                report['qualityTable'] = {}
                
        if type(report['contactInformation']) == list:
            if len(report['contactInformation']) > 0:
                report['contactInformation'] = report['contactInformation'][0]
            else:
                report['contactInformation'] = {}
        if type(report['violations']) == list:
            if len(report['violations']) > 0:
                report['violations'] = report['violations'][0]
            else:
                report['violations'] = {}
        if type(report['sourcesOfWater']) == list:
            if len(report['sourcesOfWater']) > 0:
                sources_water = report['sourcesOfWater'][0]
                sources_water_new = {}
                for key in sources_water:
                    if type(sources_water[key]) is list:
                        sources_water_new[key] = sources_water[key][0]
                    else:
                        sources_water_new[key] = sources_water[key]    
                report['sourcesOfWater'] = sources_water_new
            else:
                report['sourcesOfWater'] = {}
        if type(report['systemSusceptibility']) == list:
            if len(report['systemSusceptibility']) > 0:
                report['systemSusceptibility'] = report['systemSusceptibility'][0]
            else:
                report['systemSusceptibility'] = {}
        temp_reports.append(TempReport(report_json=report, user=user))
    if len(temp_reports) > 0:
        TempReport.objects.all().delete()
        TempReport.objects.bulk_create(temp_reports)
