# Column completer for Pandas

## Description of the software

Easily complete strings from columns in Pandas' DataFrames while using Jupyter — see the notebook for a good explanation.

This code contains a class which, once instantiated to a DataFrame, returns the column names as string corresponding to the attribute accessed with autocompletion.

It handles column names which contains spaces by replacing them with an underscore (`_`) as a default behaviour, but the replacement string can be altered upon the object instantiation.

The class definition also provides an easy way to rename the notebook columns.

## Demonstration

See the [example notebook](https://nbviewer.jupyter.org/github/AllanLRH/column_completer/blob/master/demonstration.ipynb) or the gif below — it's also avaiable in higher quality at [asciinema](https://asciinema.org/a/rv7X3EQUM8ncEMOgfZLVmFHpp).

![](column_completer.gif)
