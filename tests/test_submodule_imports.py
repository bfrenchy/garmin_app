# This works if you run `python -m tests.test_app`, but not any other way.
# Supposedly it should work on GitHub too.

from sifter_support_shared.functions.doc_loader import load_document
print(load_document)
print("Run correctly!")
