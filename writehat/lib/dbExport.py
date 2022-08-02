
import zipfile
import subprocess
from io import BytesIO
from django.conf import settings
from django.core import serializers
from writehat.lib.figure import ImageModel
from writehat.lib.revision import Revision
from writehat.lib.customer import Customer
from writehat.lib.engagement import Engagement
from writehat.lib.pageTemplate import PageTemplate
from writehat.lib.report import Report, SavedReport
from writehat.lib.findingCategory import DatabaseFindingCategory
from writehat.lib.findingGroup import CVSSFindingGroup, DREADFindingGroup, BaseFindingGroup, ProactiveFindingGroup
from writehat.lib.engagementFinding import CVSSEngagementFinding, DREADEngagementFinding, ProactiveEngagementFinding
from writehat.lib.finding import CVSSDatabaseFinding,DREADFinding, DREADDatabaseFinding, ProactiveDatabaseFinding, ProactiveFinding


MONGO_CONFIG = settings.MONGO_CONFIG

def generate_zip(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w",compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])

    return mem_zip.getvalue()

def dbExport():


    # pull mongo data
    result = subprocess.run(['mongoexport',
                             '--collection=report_components',
                             f'''--db={MONGO_CONFIG['database']}''',
                             '--host="mongo:27017"',
                             f'''--username="{MONGO_CONFIG['user']}"''',
                             f'''--password="{MONGO_CONFIG['password']}"''',
                             '--authenticationDatabase',
                              'admin', 
                              '--forceTableScan'], stdout=subprocess.PIPE)

    files = [
        ('components.json', result.stdout),
        (
            'CVSSEngagementFinding.json',
            serializers.serialize('json', CVSSEngagementFinding.objects.all()),
        ),
        (
            'DREADEngagementFinding.json',
            serializers.serialize(
                'json', DREADEngagementFinding.objects.all()
            ),
        ),
        (
            'ProactiveEngagementFinding.json',
            serializers.serialize(
                'json', ProactiveEngagementFinding.objects.all()
            ),
        ),
        (
            'DREADFindingGroup.json',
            serializers.serialize('json', DREADFindingGroup.objects.all()),
        ),
        (
            'CVSSFindingGroup.json',
            serializers.serialize('json', CVSSFindingGroup.objects.all()),
        ),
        (
            'ProactiveFindingGroup.json',
            serializers.serialize('json', ProactiveFindingGroup.objects.all()),
        ),
        (
            'BaseFindingGroup.json',
            serializers.serialize('json', BaseFindingGroup.objects.all()),
        ),
        (
            'Engagement.json',
            serializers.serialize('json', Engagement.objects.all()),
        ),
        ('Report.json', serializers.serialize('json', Report.objects.all())),
        (
            'SavedReport.json',
            serializers.serialize('json', SavedReport.objects.all()),
        ),
        (
            'PageTemplate.json',
            serializers.serialize('json', PageTemplate.objects.all()),
        ),
        (
            'CVSSDatabaseFinding.json',
            serializers.serialize('json', CVSSDatabaseFinding.objects.all()),
        ),
        (
            'DREADDatabaseFinding.json',
            serializers.serialize('json', DREADDatabaseFinding.objects.all()),
        ),
        (
            'ProactiveDatabaseFinding.json',
            serializers.serialize(
                'json', ProactiveDatabaseFinding.objects.all()
            ),
        ),
        (
            'DatabaseFindingCategory.json',
            serializers.serialize(
                'json', DatabaseFindingCategory.objects.all()
            ),
        ),
        (
            'DREADFinding.json',
            serializers.serialize('json', DREADFinding.objects.all()),
        ),
        (
            'ProactiveFinding.json',
            serializers.serialize('json', ProactiveFinding.objects.all()),
        ),
        (
            'Revision.json',
            serializers.serialize('json', Revision.objects.all()),
        ),
        (
            'Customer.json',
            serializers.serialize('json', Customer.objects.all()),
        ),
        (
            'ImageModel.json',
            serializers.serialize(
                'json',
                ImageModel.objects.all(),
                fields=[
                    "name",
                    "createdDate",
                    "modifiedDate",
                    "caption",
                    "size",
                    "findingParent",
                    "contentType",
                    "order",
                ],
            ),
        ),
    ]

    # pull images
    files.extend(
        (f'images/{image.id}.png', image.data)
        for image in ImageModel.objects.all()
    )

    return generate_zip(files)
