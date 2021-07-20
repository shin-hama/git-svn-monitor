from svn.utility import get_client

svn_client = get_client(
    r"file:///D:/workspace/test/subversion"
)

i = svn_client.info()
print(i)
