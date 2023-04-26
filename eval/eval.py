import sys
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import Terminal256Formatter
from pygments.styles import get_style_by_name
sys.path.append('../')

import joblib
store = joblib.load("store.pkl")
author = input("Enter author name ==> ")
inds = []
for item in store:
    if item["author"] == author.lower():
        inds.append(item["index"])

if len(inds) == 0:
    print("No entry found for you.")
    exit(0)

print("Methods available for you are:")
for ind in inds:
    print(str(ind))

ind = int(input("Enter the index ==> "))
if ind not in inds:
    print("Not a valid index")
    exit(0)

ref_item = ""
ref_ind = 0
count_ind = 0
for item in store:
    if item["index"] == ind:
        ref_item = item
        ref_ind = count_ind
        break
    count_ind += 1
formatter = Terminal256Formatter(style=get_style_by_name('monokai'))
print(
    f'''
Method:
------------------------

{highlight(str(ref_item["method"]), PythonLexer(), formatter)}

    
Method with Assertions:
------------------------

{highlight(str(ref_item["ground_truth"]), PythonLexer(), formatter)}

    
O/P with Naive:
------------------------

{highlight(str(ref_item["naive_op"]), PythonLexer(), formatter)}

    
O/P with Few Shot:
------------------------

{highlight(str(ref_item["few_shot_op"]), PythonLexer(), formatter)}
    '''
)
print("\n")
print("------------------------")
print("------------------------")
print("Evaluate for Naive O/P")
print("------------------------")

nv_wrong_variable = input("Is the variable wrong (y, n) => (Current : " + str(ref_item["nv_wrong_variable"])+") ")
if nv_wrong_variable.strip() != "":
    ref_item["nv_wrong_variable"] = nv_wrong_variable.lower()
nv_wrong_variable_comment = input("Comments => (Current : " + str(ref_item["nv_wrong_variable_comment"])+") ")
if nv_wrong_variable_comment.strip() != "":
    ref_item["nv_wrong_variable_comment"] = nv_wrong_variable_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_wrong_method_called = input("Is the wrong method called (y, n) => (Current : " + str(ref_item["nv_wrong_method_called"])+") ")
if nv_wrong_method_called.strip() != "":
    ref_item["nv_wrong_method_called"] = nv_wrong_method_called.lower()
nv_wrong_method_called_comment = input("Comments => (Current : " + str(ref_item["nv_wrong_method_called_comment"])+") ")
if nv_wrong_method_called_comment.strip() != "":
    ref_item["nv_wrong_method_called_comment"] = nv_wrong_method_called_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_wrong_syntax = input("Is the syntax wrong  (y, n) => (Current : " + str(ref_item["nv_wrong_syntax"])+") ")
if nv_wrong_syntax.strip() != "":
    ref_item["nv_wrong_syntax"] = nv_wrong_syntax.lower()
nv_wrong_syntax_comment = input("Comments => (Current : " + str(ref_item["nv_wrong_syntax_comment"])+") ")
if nv_wrong_syntax_comment.strip() != "":
    ref_item["nv_wrong_syntax_comment"] = nv_wrong_syntax_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_any_other_syntax_comment = input("Any other syntax Comment => (Current : " + str(ref_item["nv_any_other_syntax_comment"])+") ")
if nv_any_other_syntax_comment.strip() != "":
    ref_item["nv_any_other_syntax_comment"] = nv_any_other_syntax_comment
print() 

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_weak_assert = input("Is the assert weak (y, n) => (Current : " + str(ref_item["nv_weak_assert"])+") ")
if nv_weak_assert.strip() != "":
    ref_item["nv_weak_assert"] = nv_weak_assert.lower()
nv_weak_assert_comment = input("Comments => (Current : " + str(ref_item["nv_weak_assert_comment"])+") ")
if nv_weak_assert_comment.strip() != "":
    ref_item["nv_weak_assert_comment"] = nv_weak_assert_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_new_info = input("Is there any new info (y, n) => (Current : " + str(ref_item["nv_new_info"])+") ")
if nv_new_info.strip() != "":
    ref_item["nv_new_info"] = nv_new_info.lower()
nv_new_info_comment = input("Comments => (Current : " + str(ref_item["nv_new_info_comment"])+") ")
if nv_new_info_comment.strip() != "":
    ref_item["nv_new_info_comment"] = nv_new_info_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_wrong_location = input("Is the location wrong (y, n) => (Current : " + str(ref_item["nv_wrong_location"])+") ")
if nv_wrong_location.strip() != "":
    ref_item["nv_wrong_location"] = nv_wrong_location.lower()
nv_wrong_location_comment = input("Comments => (Current : " + str(ref_item["nv_wrong_location_comment"])+") ")
if nv_wrong_location_comment.strip() != "":
    ref_item["nv_wrong_location_comment"] = nv_wrong_location_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_wrong_assumption = input("Is the assumption wrong (y, n) => (Current : " + str(ref_item["nv_wrong_assumption"])+") ")
if nv_wrong_assumption.strip() != "":
    ref_item["nv_wrong_assumption"] = nv_wrong_assumption.lower()
nv_wrong_assumption_comment = input("Comments => (Current : " + str(ref_item["nv_wrong_assumption_comment"])+") ")
if nv_wrong_assumption_comment.strip() != "":
    ref_item["nv_wrong_assumption_comment"] = nv_wrong_assumption_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_all_covered = input("Are all assertions covered (y, n) => (Current : " + str(ref_item["nv_all_covered"])+") ")
if nv_all_covered.strip() != "":
    ref_item["nv_all_covered"] = nv_all_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_partial_covered = input("Are partial assertions covered (y, n) => (Current : " + str(ref_item["nv_partial_covered"])+") ")
if nv_partial_covered.strip() != "":
    ref_item["nv_partial_covered"] = nv_partial_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

nv_none_covered = input("Are no assertions covered (y, n) => (Current : " + str(ref_item["nv_none_covered"])+") ")
if nv_none_covered.strip() != "":
    ref_item["nv_none_covered"] = nv_none_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

print("\n")
print("\n")
print("------------------------")
print("------------------------")
print("Evaluate for Few Shot O/P")
print("------------------------")

fs_wrong_variable = input("Is the variable wrong (y, n) => (Current : " + str(ref_item["fs_wrong_variable"])+") ")
if fs_wrong_variable.strip() != "":
    ref_item["fs_wrong_variable"] = fs_wrong_variable.lower()
fs_wrong_variable_comment = input("Comments => (Current : " + str(ref_item["fs_wrong_variable_comment"])+") ")
if fs_wrong_variable_comment.strip() != "":
    ref_item["fs_wrong_variable_comment"] = fs_wrong_variable_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_wrong_method_called = input("Is the wrong method called (y, n) => (Current : " + str(ref_item["fs_wrong_method_called"])+") ")
if fs_wrong_method_called.strip() != "":
    ref_item["fs_wrong_method_called"] = fs_wrong_method_called.lower()
fs_wrong_method_called_comment = input("Comments => (Current : " + str(ref_item["fs_wrong_method_called_comment"])+") ")
if fs_wrong_method_called_comment.strip() != "":
    ref_item["fs_wrong_method_called_comment"] = fs_wrong_method_called_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_wrong_syntax = input("Is the syntax wrong  (y, n) => (Current : " + str(ref_item["fs_wrong_syntax"])+") ")
if fs_wrong_syntax.strip() != "":
    ref_item["fs_wrong_syntax"] = fs_wrong_syntax.lower()
fs_wrong_syntax_comment = input("Comments => (Current : " + str(ref_item["fs_wrong_syntax_comment"])+") ")
if fs_wrong_syntax_comment.strip() != "":
    ref_item["fs_wrong_syntax_comment"] = fs_wrong_syntax_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_any_other_syntax_comment = input("Any other syntax Comment => (Current : " + str(ref_item["fs_any_other_syntax_comment"])+") ")
if fs_any_other_syntax_comment.strip() != "":
    ref_item["fs_any_other_syntax_comment"] = fs_any_other_syntax_comment
print() 

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_weak_assert = input("Is the assert weak (y, n) => (Current : " + str(ref_item["fs_weak_assert"])+") ")
if fs_weak_assert.strip() != "":
    ref_item["fs_weak_assert"] = fs_weak_assert.lower()
fs_weak_assert_comment = input("Comments => (Current : " + str(ref_item["fs_weak_assert_comment"])+") ")
if fs_weak_assert_comment.strip() != "":
    ref_item["fs_weak_assert_comment"] = fs_weak_assert_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_new_info = input("Is there any new info (y, n) => (Current : " + str(ref_item["fs_new_info"])+") ")
if fs_new_info.strip() != "":
    ref_item["fs_new_info"] = fs_new_info.lower()
fs_new_info_comment = input("Comments => (Current : " + str(ref_item["fs_new_info_comment"])+") ")
if fs_new_info_comment.strip() != "":
    ref_item["fs_new_info_comment"] = fs_new_info_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_wrong_location = input("Is the location wrong (y, n) => (Current : " + str(ref_item["fs_wrong_location"])+") ")
if fs_wrong_location.strip() != "":
    ref_item["fs_wrong_location"] = fs_wrong_location.lower()
fs_wrong_location_comment = input("Comments => (Current : " + str(ref_item["fs_wrong_location_comment"])+") ")
if fs_wrong_location_comment.strip() != "":
    ref_item["fs_wrong_location_comment"] = fs_wrong_location_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_wrong_assumption = input("Is the assumption wrong (y, n) => (Current : " + str(ref_item["fs_wrong_assumption"])+") ")
if fs_wrong_assumption.strip() != "":
    ref_item["fs_wrong_assumption"] = fs_wrong_assumption.lower()
fs_wrong_assumption_comment = input("Comments => (Current : " + str(ref_item["fs_wrong_assumption_comment"])+") ")
if fs_wrong_assumption_comment.strip() != "":
    ref_item["fs_wrong_assumption_comment"] = fs_wrong_assumption_comment
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_all_covered = input("Are all assertions covered (y, n) => (Current : " + str(ref_item["fs_all_covered"])+") ")
if fs_all_covered.strip() != "":
    ref_item["fs_all_covered"] = fs_all_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_partial_covered = input("Are partial assertions covered (y, n) => (Current : " + str(ref_item["fs_partial_covered"])+") ")
if fs_partial_covered.strip() != "":
    ref_item["fs_partial_covered"] = fs_partial_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")

fs_none_covered = input("Are no assertions covered (y, n) => (Current : " + str(ref_item["fs_none_covered"])+") ")
if fs_none_covered.strip() != "":
    ref_item["fs_none_covered"] = fs_none_covered.lower()
print()

store[ref_ind] = ref_item
joblib.dump(store, "store.pkl")