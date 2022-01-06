from PyDictionary import PyDictionary

def word_meaning(query):
    rem_l = ['what','is','the','meaning','means',' ','of']
    for i in rem_l:
        query = query.replace(i, '',1)
    if query=='':
        return 'not found'
    try:
        dicts = PyDictionary.meaning(query)
        if not isinstance(dicts, dict):
            raise AttributeError()
    except:
        return 'error'
    else:
        try:
            rs =  ','.join(dicts[list(dicts.keys())[0]])
        except:
            return 'error'
        else:
            return rs