from archicad import ACConnection

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

################################ CONFIGURATION #################################
moveToFolder = False
renameView = True
viewSuffix = '<unused>'
folderName = '-- UnusedViews --'
renameFolderFromPreviousRun = True
folderNameForPreviousRun = '-- Previous UnusedViews --'
################################################################################


def isLinkNavigatorItem(item : act.NavigatorItem):
    return item.sourceNavigatorItemId is not None


layoutBookTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('LayoutBook'))
links = acu.FindInNavigatorItemTree(layoutBookTree.rootItem, isLinkNavigatorItem)

for publisherSetName in acc.GetPublisherSetNames():
	publisherSetTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('PublisherSets', publisherSetName))
	links += acu.FindInNavigatorItemTree(publisherSetTree.rootItem, isLinkNavigatorItem)

sourcesOfLinks = set(link.sourceNavigatorItemId.guid for link in links)

viewMapTree = acc.GetNavigatorItemTree(act.NavigatorTreeId('ViewMap'))
unusedViewTreeItems = acu.FindInNavigatorItemTree(viewMapTree.rootItem,
    lambda node: node.name != folderName and node.name != folderNameForPreviousRun and
        not acu.FindInNavigatorItemTree(node, lambda i: i.navigatorItemId.guid in sourcesOfLinks)
    )
unusedViewTreeItemsFiltered = []
for ii in unusedViewTreeItems:
    isChildOfUnused = False
    for jj in unusedViewTreeItems:
        if ii != jj and acu.FindInNavigatorItemTree(jj, lambda node: node.navigatorItemId.guid == ii.navigatorItemId.guid):
            isChildOfUnused = True
            break
    if not isChildOfUnused:
        unusedViewTreeItemsFiltered.append(ii)
unusedViewTreeItems = unusedViewTreeItemsFiltered

folderFromPreviousRun = acu.FindInNavigatorItemTree(viewMapTree.rootItem, lambda i: i.name == folderName)
if folderFromPreviousRun and renameFolderFromPreviousRun:
    acc.RenameNavigatorItem(folderFromPreviousRun[0].navigatorItemId, newName=folderNameForPreviousRun)

unusedViewsFolder = None
if moveToFolder:
    if not renameFolderFromPreviousRun and folderFromPreviousRun:
        unusedViewsFolder = folderFromPreviousRun[0].navigatorItemId
    else:
        unusedViewsFolder = acc.CreateViewMapFolder(act.FolderParameters(folderName))

for item in sorted(unusedViewTreeItems, key=lambda i: i.prefix + i.name):
    try:
        if moveToFolder and unusedViewsFolder:
            acc.MoveNavigatorItem(item.navigatorItemId, unusedViewsFolder)
        if renameView:                                                                          #new command for renaming views:
            acc.RenameNavigatorItem(item.navigatorItemId, newName=item.name+viewSuffix)         #use RenameNavigatorItem to rename views filtered from previous steps. new name = old name + suffix
        print(f"{item.prefix} {item.name}\n\t{item}")
    except:
        continue

