class ColumnCompleter(object):
    """Complete Pandas DataFrame column names"""

    def __init__(self, df, space_filler='_', silence_warnings=False):
        """
        Once instantiated with a Pandas DataFrame, it will expose the column 
        names as attributes which maps to their string counterparts.
        Autocompletion is supported.

        Spaces in the column names are by default replaced with underscores, though
        it still maps to the original column names — the replacement is necessary to
        conform to a valid Python syntax.

        Parameters
        ----------
        df : pd.DataFrame   
            DataFrame whose column names to expose.
        space_filler : str, optional
            String to replace spaces in collumn names, by default '_'.
        silence_warnings : bool, optional
            Set to True to disable warning concerning column names which start or ends 
            with spaces, which is hard to detect by visual inspection, by default False.
        """
        super(ColumnCompleter, self).__init__()
        self.columns = df.columns
        self.space_filler = space_filler
        self.silence_warnings = silence_warnings
        if not self.silence_warnings:
            self._warn_about_column_names_edge_spaces()
        self._set_columns()

    def _warn_about_column_names_edge_spaces(self):
        if not hasattr(self.columns, 'str'):  # the column names are not strings
            return None
        if self.columns.str.startswith(' ').any():
            raise Warning("The following columns starts with one or more spaces: " +
                          self.columns[self.columns.str.startswith(' ')])
        if self.columns.str.endswith(' ').any():
            raise Warning("The following columns ends with one or more spaces: " +
                          self.columns[self.columns.str.endswith(' ')])

    def _set_columns(self):
        if not hasattr(self.columns, 'str'):  # the column names are not strings
            self.mapping = {col: col for col in self.columns}
        elif self.space_filler is None:
            self.mapping = {col: col for col in self.columns if ' ' not in col}
        else:
            self.mapping = {col.replace(
                ' ', self.space_filler): col for col in self.columns}
            if len(self.mapping) < len(self.columns):
                raise ValueError("Using {} as a replacemnt for".format(repr(self.space_filler)) +
                                 " spaces causes a collision of column names, please chose another.")
        self.keys = self.mapping.keys()
        if len(self.keys) < len(self.columns) and not self.silence_warnings:
            raise Warning("Without a space_filler specified, you're only able to autocomplete " +
                          "{} of {} column names.".format(len(self.keys), len(self.columns)))

    @staticmethod
    def replace_df_column_spaces(df, rep, capatilize_first_letter=False):
        """
        Return a DataFrame with the spaces in the column names replaced with a custom string.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame whose columns ot rename.
        rep : str
            String to replace spaces with.
        capatilize_first_letter : bool, optional
            If True, the first letter of the rennamed columns will be capitalized, by default False.

        Returns
        -------
        pd.DataFrame
            DataFrame with renamed columns.

        Raises
        ------
        ValueError
            If the renaming of the columns causes one or more column names to be identical.
        """
        rename_dict = {col: col.replace(' ', rep) for col in df.columns}
        if len(set(rename_dict.values())) < len(df.columns.unique()):
            raise ValueError("Renaming the columns in such a way would cause a " +
                             "collision of column names.")
        if capatilize_first_letter:
            rename_dict = {k: v[0].upper() + v[1:]
                           for k, v in rename_dict.items()}
        return df.rename(columns=rename_dict)

    def __dir__(self):
        return self.keys

    def __getattr__(self, key):
        return self.mapping[key]
