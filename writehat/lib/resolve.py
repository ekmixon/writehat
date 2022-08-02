import logging
from writehat.lib.figure import ImageModel
from writehat.lib.revision import Revision
from writehat.lib.engagement import Engagement
from writehat.components.base import BaseComponent
from writehat.lib.pageTemplate import PageTemplate
from writehat.lib.report import Report, SavedReport
from writehat.lib.errors import ComponentError, DatabaseError
from writehat.lib.findingCategory import DatabaseFindingCategory
from writehat.lib.findingGroup import CVSSFindingGroup, DREADFindingGroup, BaseFindingGroup, ProactiveFindingGroup
from writehat.lib.engagementFinding import CVSSEngagementFinding, DREADEngagementFinding, ProactiveEngagementFinding
from writehat.lib.finding import CVSSDatabaseFinding, ProactiveFinding, ProactiveDatabaseFinding, DREADDatabaseFinding

log = logging.getLogger(__name__)


allModels = {
    'cvssengagementfinding': CVSSEngagementFinding,
    'dreadengagementfinding': DREADEngagementFinding,
    'proactivefinding': ProactiveFinding,
    'engagement': Engagement,
    'report': Report,
    'savedreport': SavedReport,
    'pagetemplate': PageTemplate,
    'cvssdatabasefinding': CVSSDatabaseFinding,
    'dreaddatabasefinding': DREADDatabaseFinding,
    'dreadfindinggroup': DREADFindingGroup,
    'cvssfindinggroup': CVSSFindingGroup,
    'basefindinggroup': BaseFindingGroup,
    'databasefindingcategory': DatabaseFindingCategory,
    'proactivefindinggroup': ProactiveFindingGroup,
    'proactivedatabasefinding': ProactiveDatabaseFinding,
    'proactiveengagementfinding': ProactiveEngagementFinding,
    'imagemodel': ImageModel,
    'revision': Revision,
    'reportcomponent': BaseComponent,
    'component': BaseComponent
}

def resolve(uuid, hint=''):

    if hints := hint.lower().split():
        if len(hints) == 1 and hint[0] in allModels:
            return allModels[hint].get(id=uuid)

        for modelName, modelCandidate in allModels.items():
                # if all hints match
            if all(h in modelName for h in hints):
                if modelName == 'reportcomponent':
                    try:
                        return modelCandidate.get(id=uuid)
                    except ComponentError:
                        pass
                else:
                    try:
                        return modelCandidate.get(id=uuid)
                    except modelCandidate.DoesNotExist:
                        pass

    else:
        for modelName, modelCandidate in allModels.items():
            if modelName in ('component', 'reportcomponent'):
                try:
                    return modelCandidate.get(id=uuid)
                except ComponentError:
                    pass
            else:
                try:
                    return modelCandidate.get(id=uuid)
                except modelCandidate.DoesNotExist:
                    pass

    #no matches found, raise an error
    log.debug(f"GUID ({id})did not match any models using the provided hint: {hint}")
    raise DatabaseError("GUID did not match any models using the provided hint")


def resolve_filter(*args, **kwargs):
    '''
    The same as resolve(), except it uses Django's model.objects.filter
    yields multiple instantiated models
    '''

    hints = kwargs.pop('hint', '').lower().split()
    results = []

    if hints:
        # check for an exact match
        if len(hints) == 1 and hint[0] in allModels:
            results.extend(iter(allModels[hint].objects.filter(*args, **kwargs)))
        else:
            for modelName, modelCandidate in allModels.items():
                # if all hints match
                if all(h in modelName for h in hints) and modelName not in (
                    'reportcomponent',
                ):
                    try:
                        results.extend(iter(modelCandidate.objects.filter(*args, **kwargs)))
                    except modelCandidate.DoesNotExist:
                        pass

    else:
        for modelName, modelCandidate in allModels.items():
            if modelName not in ('reportcomponent',):
                try:
                    results.extend(iter(modelCandidate.objects.filter(*args, **kwargs)))
                except modelCandidate.DoesNotExist:
                    pass

    log.debug(f"resolve_filter() found {len(results):,} models using the provided hint: {hint}")
    return results