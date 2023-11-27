from iccr.models import TempReport
from rest_framework import serializers


class TempReportSerializer(serializers.ModelSerializer):
    report_json = serializers.JSONField()

    def validate(self, data):
        report_json = data['report_json']
        publicNotificationRuleData = report_json['violations']['publicNotificationRule']
        publicNotificationRules = []

        for item in publicNotificationRuleData:
            pNR = {
                'violationType': item[0],
                'violationBegin': item[1],
                'violationEnd': item[2],
                'violationExplanation': item[3]
            }
            count = 0
            for k in pNR:
                if pNR[k] != '':
                    count += 1
            if count != 0:
                publicNotificationRules.append(pNR)

        revisedTotalColiformRuleData = report_json['violations']['revisedTotalColiformRule']
        revisedTotalColiformRules = []
        for item in revisedTotalColiformRuleData:
            rTCR = {
                'violationType': item[0],
                'violationBegin': item[1],
                'violationEnd': item[2],
                'violationExplanation': item[3]
            }
            count = 0
            for k in rTCR:
                if rTCR[k] != '':
                    count += 1
            if count != 0:
                revisedTotalColiformRules.append(rTCR)

        data['report_json'] = {
            'userId': report_json['userId'],
            'userName': report_json['userName'],
            'title': report_json['title'],
            'nameOfUtility': report_json['nameOfUtility'],
            'nameOfReport': report_json['nameOfReport'],
            'additionalHealthInformation': report_json['additionalHealthInformation'],
            'microbialContaminants': report_json['microbialContaminants'],
            'radioactiveContaminants': report_json['radioactiveContaminants'],
            'pesticidesContaminants': report_json['pesticidesContaminants'],
            'organicContaminants': report_json['organicContaminants'],
            'howToReachOut': report_json['howToReachOut'],
            'contactInformation': report_json['contactInformation'],
            'overallWaterQuality': report_json['overallWaterQuality'],
            'overallWaterQualityText': report_json['overallWaterQualityText'],
            'sourceWaterAssessment': report_json['sourceWaterAssessment'],
            'violations': {
                'publicNotificationRule': publicNotificationRules,
                'revisedTotalColiformRule': revisedTotalColiformRules
            },
            'sourcesOfWater': report_json['sourcesOfWater'],
            'qualityTable': report_json['qualityTable'],
            'systemSusceptibility': report_json['systemSusceptibility']
        }
        return data

    class Meta:
        model = TempReport
        fields = ('id', 'report_json', 'user')
        read_only_fields = ('user', )
