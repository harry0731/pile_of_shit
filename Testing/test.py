import pandas as pd

d = ['A688EDBD',
'2E23AD4A',
'A688EDBD',
'2E23AD4A',
'66BFEDBD',
'5E0CB04A',
'C612A3B6',
'66BD727D',
'66FDA4B6',
'8629A6B6',
'ED7C46D2',
'DD423CD2',
'1D103AD2',
'4DD942D2',
'5E7BAD4A',
'EEDCAE4A',
'2BB112B3',
'B2859117',
'2B7C13B3',
'EB06E5B3',
'8D013FD2']

print(d[0][2])


for da in d:
	b = da[6]+da[7]+da[4]+da[5]+da[2]+da[3]+da[0]+da[1]
	print(b.lower())