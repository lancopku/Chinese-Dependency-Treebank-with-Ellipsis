import os
import sys

from argparse import ArgumentParser

import requests

ID = 0
FORM = 1
POS = 4
HEAD = 6
DEP = 7


class StanfordCoreNLP:
    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.lang = 'zh'

        self.properties = {
            'annotators': 'tokenize,ssplit,pos,depparse',
            'outputFormat': 'conllu',
            'tokenize.language': 'Whitespace',
            'ssplit.eolonly': 'true'
        }

        self.url = self.host + ':' + str(self.port)

    def annotate(self, text):
        if sys.version_info.major >= 3:
            text = text.encode('utf-8')

        r = requests.post(
            self.url,
            params={
                'properties': str(self.properties),
                'pipelineLanguage': self.lang
            },
            data=text,
            headers={'Connection': 'close'})
        return r.text


class Token(object):
    def __init__(self, id_, form, omit, head):
        self.id = id_
        self.form = form
        self.omit = omit
        self.pos = None
        self.head = head
        self.rel = None
        self.ppos = None
        self.phead = None
        self.prel = None
        self.no_ppos = None
        self.no_phead = None
        self.no_prel = None

    def __str__(self):
        return '\t'.join([
            x if x is not None else '_' for x in [
                self.id, self.form, self.omit, self.pos, self.head, self.rel,
                self.no_ppos, self.no_phead, self.no_prel, self.ppos,
                self.phead, self.prel
            ]
        ])


def aug_sent(sent, nlp):
    sent_str = ' '.join([token.form for token in sent])
    res = nlp.annotate(sent_str)
    for i, line in enumerate(res.split('\n')):
        line = line.strip()
        if not line:
            break
        anns = line.split('\t')
        sent[i].ppos = anns[POS]
        sent[i].phead = anns[HEAD]
        sent[i].prel = anns[DEP]

    no_sent = [token for token in sent if token.omit != 'I']
    no_sent_str = ' '.join([token.form for token in no_sent])
    res = nlp.annotate(no_sent_str)
    for i, line in enumerate(res.split('\n')):
        line = line.strip()
        if not line:
            break
        anns = line.split('\t')
        no_sent[i].no_ppos = anns[POS]
        if anns[HEAD] != '0':
            no_sent[i].no_phead = no_sent[int(anns[HEAD]) - 1].id
        else:
            no_sent[i].no_phead = anns[HEAD]
        no_sent[i].no_prel = anns[DEP]
    return sent


def aug_file(fp, nlp):
    outp, ext = os.path.splitext(fp)
    outp = outp + '.aug' + ext
    sent = []
    with open(fp, encoding='utf-8', mode='r') as fin:
        with open(outp, mode='w', encoding='utf-8', newline='\n') as fout:
            for line in fin:
                line = line.strip()
                if line:
                    sent.append(Token(*line.split('\t')))
                else:
                    if sent:
                        aug_sent(sent, nlp)
                        fout.write('# {}\n'.format(' '.join([
                            token.form
                            if token.omit == 'O' else '_' + token.form + '_'
                            for token in sent
                        ])))
                        fout.write(''.join(
                            [str(token) + '\n' for token in sent]))
                        sent = []
                    fout.write('\n')


def main():

    argparser = ArgumentParser(epilog=
        'You should check the VALIDITY of the arguments. The script does not check them, and will fail with no warning.'
    )
    argparser.add_argument(
        'host',
        type=str,
        help=
        'Host address of the Stanford CoreNLP server. Do not include the trailing slash.'
    )
    argparser.add_argument(
        'port', type=int, help='Port of the Stanford CoreNLP server.')
    argparser.add_argument(
        'filepath',
        type=str,
        help=
        'Filepath of the tsv file to be augmented using Stanford CoreNLP pipeline.'
    )
    args = argparser.parse_args()

    nlp = StanfordCoreNLP(args.host, args.port)
    aug_file(args.filepath, nlp)


if __name__ == '__main__':
    main()
