# An Ellipsis-aware Chinese Dependency Treebank for Web Text

The dataset accompanies the paper _Building an Ellipsis-aware Chinese Dependency Treebank for Web Text_ [[pdf]](http://www.lrec-conf.org/proceedings/lrec2018/pdf/297.pdf) by Xuancheng Ren, Xu Sun, Ji Wen, Bingzhen Wei, Weidong Zhan, and Zhiyuan Zhang at [LREC 2018](http://www.lrec-conf.org/proceedings/lrec2018/index.html).

# Introduction

Web 2.0 has brought with it numerous user-produced data revealing one's thoughts, experiences, and knowledge, which are a great source for many tasks, such as information extraction, and knowledge base construction. However, the colloquial nature of the texts poses new challenges for current natural language processing techniques, which are more adapt to the formal form of the language. Ellipsis is a common linguistic phenomenon that some words are left out as they are understood from the context, especially in oral utterance, hindering the improvement of dependency parsing, which is of great importance for tasks relied on the meaning of the sentence. In order to promote research in this area, we are releasing a Chinese dependency treebank of 319 weibos, containing 572 sentences with omissions restored and contexts reserved.

The detailed description of the treebank and the annotation procedure is at [[arxiv]](https://arxiv.org/abs/1801.06613) and [[lrec2018]](http://www.lrec-conf.org/proceedings/lrec2018/summaries/297.html). An example of the annotation procedure is shown below

![An Example of the annotation procedure](./doc/ex.png)

# Statistics of the Treebank

| Type          | #Token | #Word | #Sentence | #Weibo |
| ------------- | -------: | ------: | ----------: | -------: |
| Original      |   12,508 |   8,382 |         572 |      319 |
| Ellipsis      |      256 |     208 |         162 |      122 |
| Overall       |   12,764 |   8,590 |         572 |      319 |
| Percentage(%) |     2.01 |    2.42 |       28.32 |    38.24 |

We are releasing a first version of the dataset, containing 8,590 tokens, 572 sentences, and 319 weibos (Table 1). The raw text is from [LWC](http://lwc.daanvanesch.nl/), a weibo corpus. Unsurprisingly, due to the characteristics of microblogging, the average length of the sentences are quite short, around 15.0 tokens per sentence, comparing to 27.0 tokens per sentence in CTB5. We have restored 256 characters and 208 words in the dataset. As shown in the table above, ellipsis is indeed a common phenomenon in web text, which requires more attention, as 162 of the sentences, and 122 of the weibos contain ellipsis, meaning 38.24% of the weibos involve ellipsis.

There are total 8,018 dependencies (excluding the root). 7,762 of them are from an original token to an original token, 187 of them are from an original token to an omitted token, 61 of them are from an omitted token to an original token, and 8 of them are from an omitted token to an omitted token. 

# Annotation Format

The annotation files are converted to a single file in the tsv format. There are four columns in the file. 
- The first column is the token's index in the sentence, starting from 1. 
- The second column is the textual form of the token. 
- The third column indicates whether the token is a restored one. 'O' stands for original tokens, and 'I' stands for restored tokens. 
- The fourth column is the head of the token. 0 indicates the token is the root. 

There is an empty line between sentences, and an extra empty line between weibos.

# Files with Augmented Annotations

Although we have not annotated the part-of-speech tag of the tokens and the type of the dependencies, they are valuable resources for systems using the treebank. To help with the issue, we used the Stanford CoreNLP tools (version 3.9.1) with the pre-trained models to augment the annotations with part-of-speech tags (CTB version) and the type of the dependencies (UD version). The augmented file is suffixed with '_.aug_'. 

There are 12 columns in the file.
- 1: index of the token from 1
- 2：token
- 3: 'I' for restored tokens, and 'O' for original tokens
- 4: '_' (should be the POS tag)
- 5: index of its head
- 6: '_' (shoul be the type of the dependency)
- 7: POS tag, predicted without the restored tokens
- 8: index of the head, predicted without the restored tokens but indexing with the restored tokens
- 9: type of the dependency, predicted without the restored tokens
- 10: POS tag, predicted with the restored tokens
- 11: index of the head, predicted with the restored tokens 
- 12: type of the dependency, predicted with the restored tokens

However, please do keep in mind that the augmented annotaions are only for reference. While the POS tags should be generally okay, the automatically generated dependency can be very different from our annotation (Note: We annotated the dependency basically following the UD dependency guideline, so the annoation difference should not be a major problem for the parser).

The python script for processing is provided in the _utils_ folder.

# Citation

If you use this dataset for your research, please cite this paper as

```
@inproceedings{ren2018ellipsis,
  author    = {Xuancheng Ren and
               Xu Sun and
               Ji Wen and
               Bingzhen Wei and
               Weidong Zhan and
               Zhiyuan Zhang},
  title     = {Building an Ellipsis-aware Chinese Dependency Treebank for Web Text},
  booktitle = {Proceedings of the Eleventh International Conference on Language Resources
               and Evaluation {LREC} 2018, Miyazaki, Japan, May 7-12, 2018},
  publisher = {European Language Resources Association {(ELRA)}},
  isbn      = {979-10-95546-00-9},
  year      = {2018}
}
```
