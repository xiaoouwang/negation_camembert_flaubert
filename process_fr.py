import re


def process_negsimp(tsvfile, mask_tok=True):
    nkdict = {}
    inputlist = []
    tgtlist = []
    i = 0
    csvclean = []
    with open(tsvfile, 'r') as f:
        for line in f:
            it, affsent, negsent, afftgt, negtgt = [
                # e.strip() for e in line.strip().split('\,')]
                e.strip() for e in line.strip().split(',')]
            affsent = re.sub(' \(.+\)', '', affsent)
            negsent = re.sub(' \(.+\)', '', negsent)
            if it == 'item':
                continue
            for sent, tgt, cond in [(affsent, afftgt, 'TA'), (negsent, afftgt, 'FN'), (affsent, negtgt, 'FA'), (negsent, negtgt, 'TN')]:
                nkdict[i] = {}
                if mask_tok:
                    context = ' '.join([sent, '<mask>'])
                else:
                    context = ' '.join([sent])
                nkdict[i]['sent'] = context
                nkdict[i]['tgt'] = tgt
                nkdict[i]['item'] = it
                nkdict[i]['cond'] = cond
                if cond in ('TA', 'FA'):
                    nkdict[i]['exp'] = afftgt
                else:
                    nkdict[i]['exp'] = negtgt
                nkdict[i]['options'] = afftgt+" "+negtgt
                inputlist.append(context)
                tgtlist.append(tgt)
                i += 1
    return inputlist, tgtlist, nkdict
