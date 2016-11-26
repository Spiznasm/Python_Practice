def merge(line):
    merge_tool = dict()
    keys = range(len(line))
    for key in keys:
        merge_tool[key]=[line[key],False]

    for key in merge_tool:
        if key == 0:
            pass
        elif merge_tool[key-1] == 0:
            merge_tool[key-1]=merge_tool[key]
        elif merge_tool[key-1]==merge_tool[key]:
            merge_tool[key-1]=merge_tool[key]*2
        else:
            pass

    print merge_tool

