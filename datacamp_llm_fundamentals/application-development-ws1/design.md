output model design:

1) ndc_numbers as a list of strings, required

2) product_name a string, required

3) dosage_form a string, optional

4) strength a string, optional

Input  A single string from the Product Description field of an FDA Drug recall notice.

Examples

example01 = 

“““\
Isotretinoin Capsules, USP, 30 mg, Rx Only, 10 count Prescription Pack, Manufactured for: Teva Pharmaceuticals USA, Inc., Parsippany, NJ 07054, NDC 0591-2435-15 (carton), NDC 0591-2435-45 (blister pack).

“““

example02 =

“““

Isotretinoin Capsules, USP, 40 mg, 10 count Prescription Pacs, Rx only, Manufactured for: Teva Pharmaceuticals USA, Inc., Parsippany, NJ 07054, NDC 0591-2436-15 (carton), NDC 0591-2436-45 (blister pack).

“““

example03 =

“““

Dexamethasone Sodium Phosphate Injection, USP, 100 mg/ 10 mL, (10 mg/mL), 10x10 mL Multiple Dose Vials, Rx only, Manufactured for: Somerset Therapeutics, LLC., Somerset, NJ 08873, NDC carton: 70069-025-10; NDC vial: 70069-025-01

“““