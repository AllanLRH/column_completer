class ColumnCompleter(object):
    """Complete Pandas DataFrame column names"""
    def __init__(self, df, space_filler='_', silence_warnings=False):
        super(ColumnCompleter, self).__init__()
        self.columns = df.columns
        self.space_filler = space_filler
        self.silence_warnings = silence_warnings
        if not self.silence_warnings:
            self.warn_about_column_names_edge_spaces()
        self.set_columns()


    def warn_about_column_names_edge_spaces(self):
        if not hasattr(self.columns, 'str'):
            return None
        if self.columns.str.startswith(' ').any():
            raise Warning("The following columns starts with one or more spaces: " +
                           self.columns[self.columns.str.startswith(' ')])
        if self.columns.str.endswith(' ').any():
            raise Warning("The following columns ends with one or more spaces: " +
                           self.columns[self.columns.str.endswith(' ')])

    def set_columns(self):
        if self.space_filler is None:
            self.mapping = {col: col for col in self.columns if ' ' not in col}
        else:
            self.mapping = {col.replace(' ', self.space_filler):col for col in self.columns}
            if len(self.mapping) < len(self.columns):
                raise ValueError("Using {} as a replacemnt for".format(repr(self.space_filler)) +
                    " spaces causes a collision of column names, please chose another.")
        self.keys = self.mapping.keys()
        if len(self.keys) < len(self.columns) and not self.silence_warnings:
            raise Warning("Without a space_filler specified, you're only able to autocomplete " +
                "{} of {} column names.".format(len(self.keys), len(self.columns)))

    @staticmethod
    def replace_df_column_spaces(df, rep, capatilize_first_letter=False):
        rename_dict = {col: col.replace(' ', rep) for col in df.columns}
        if len(set(rename_dict.values())) < len(df.columns.unique()):
            raise ValueError("Renaming the columns in such a way would cause a " +
                "collision of column names.")
        if capatilize_first_letter:
            rename_dict = {k: v[0].upper() + v[1:] for k, v in rename_dict.items()}
        return df.rename(columns=rename_dict)

    def __dir__(self):
        return self.keys

    def __getattr__(self, key):
        return self.mapping[key]
