
from delphin.derivation import Derivation
from delphin.mrs import (
    Mrs,
    Dmrs,
    simplemrs,
    eds,
)

try:
    stringtypes = (str, unicode)  # Python 2
except NameError:
    stringtypes = (str,)  # Python 3

class ParseResult(dict):
    """
    A wrapper around a result dictionary to automate deserialization
    for supported formats. A ParseResult is still a dictionary, so the
    raw data can be obtained using dict access.
    """

    def __repr__(self):
        return 'ParseResult({})'.format(dict.__repr__(self))

    def derivation(self):
        """
        Deserialize and return a Derivation object for UDF- or
        JSON-formatted derivation data; otherwise return the original
        string.
        """
        drv = self.get('derivation')
        if drv is not None:
            if isinstance(drv, dict):
                drv = Derivation.from_dict(drv)
            elif isinstance(drv, stringtypes):
                drv = Derivation.from_string(drv)
        return drv

    def mrs(self):
        """
        Deserialize and return an Mrs object for simplemrs or
        JSON-formatted MRS data; otherwise return the original string.
        """
        mrs = self.get('mrs')
        if mrs is not None:
            if isinstance(mrs, dict):
                mrs = Mrs.from_dict(mrs)
            elif isinstance(mrs, stringtypes):
                mrs = simplemrs.loads_one(mrs)
        return mrs

    def eds(self):
        """
        Deserialize and return an Eds object for native- or
        JSON-formatted EDS data; otherwise return the original string.
        """
        _eds = self.get('eds')
        if _eds is not None:
            if isinstance(_eds, dict):
                _eds = eds.Eds.from_dict(_eds)
            elif isinstance(_eds, stringtypes):
                _eds = eds.loads_one(_eds)
        return _eds

    def dmrs(self):
        """
        Deserialize and return a Dmrs object for JSON-formatted DMRS
        data; otherwise return the original string.
        """
        dmrs = self.get('dmrs')
        if dmrs is not None:
            if isinstance(dmrs, dict):
                dmrs = Dmrs.from_dict(dmrs)
        return dmrs

class ParseResponse(dict):
    """
    A wrapper around the response dictionary for more convenient
    access to results.
    """
    _result_factory = ParseResult

    def __repr__(self):
        return 'ParseResponse({})'.format(dict.__repr__(self))

    def results(self):
        """Return ParseResult objects for each result."""
        return [self._result_factory(r) for r in self.get('results', [])]

    def result(self, i):
        """Return a ParseResult object for the *i*th result."""
        return self._result_factory(self.get('results', [])[i])