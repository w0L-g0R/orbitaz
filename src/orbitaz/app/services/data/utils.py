from pysftp import Connection


def check_if_sftp_remotepath_exists(sftp: Connection, remotepath: str):

    """
    This error checking function requires a running sftp connection.
    """

    if sftp.exists(remotepath=remotepath):
        return True
    else:
        raise IOError(
            f"{remotepath} seems not to exist. Did you check spelling errors?"
        )
    return