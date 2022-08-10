import pkg_resources
import pandas as pd

def load_lalonde():
    """Data from National Supported Work Demonstration and PSID, as analyzed by Dehejia and Wahba (1999).

    Contains the following fields:
        treat           non-null int64
        age             non-null int64
        educ            non-null int64
    ... (docstring truncated) ...

    """
    # This is a stream-like object. If you want the actual info, call
    # stream.read()
    stream = pkg_resources.resource_stream(__name__, 'data/lalonde.csv')
    return pd.read_csv(stream, index_col=0)

