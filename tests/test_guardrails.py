"""Small adversarial checks for consequential selection and inference failures."""
from pathlib import Path
import sys
import unittest
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from extraction import deduplicate
from analysis import fit_logit

class GuardrailTests(unittest.TestCase):
    def rows(self, values, dates=None):
        rows=[]
        for i,value in enumerate(values):
            rows.append(dict(adsh='a',tag='Assets',version='us-gaap/2025',ddate='20251231',
                qtrs='0',uom='USD',dimh='0x00000000',iprx=str(i),value=value,
                footnote=pd.NA,coreg=pd.NA,datp=(dates or ['0']*len(values))[i],durp='0',dimn='0',dcml='0'))
        return pd.DataFrame(rows,dtype='string')

    def test_equal_precision_conflict_not_selected(self):
        # Intervals touch, but same declared precision with unequal values is inconsistent.
        selected,audit=deduplicate(self.rows(['100','101']))
        self.assertEqual(audit.duplicate_status.iloc[0],'REVIEW_INCONSISTENT_VALUES')
        self.assertEqual(len(selected),0)

    def test_context_conflict_not_selected(self):
        selected,audit=deduplicate(self.rows(['100','100'],['0','1']))
        self.assertEqual(audit.duplicate_status.iloc[0],'REVIEW_CONTEXT_CONFLICT')
        self.assertEqual(len(selected),0)

    def test_reported_zero_is_not_nil(self):
        selected,_=deduplicate(self.rows(['0','0']))
        self.assertEqual(selected.value_num.iloc[0],0)
        selected,audit=deduplicate(self.rows([pd.NA,pd.NA]))
        self.assertTrue(pd.isna(selected.value_num.iloc[0]))
        self.assertEqual(audit.duplicate_status.iloc[0],'ALL_MISSING')

    def test_separation_stops_model(self):
        s=pd.DataFrame({'PositiveCashTax':[0]*30+[1]*30,'LogAssets':np.arange(60),
            'cik':list(map(str,range(60))), 'TotalRevenue_definition':['STANDARD_CONSOLIDATED_TOTAL']*60})
        result,_,info=fit_logit(s,pd.Series(True,index=s.index),['LogAssets'],'test')
        self.assertTrue(result.empty)
        self.assertEqual(info['reason'],'COMPLETE_OR_QUASI_SEPARATION')

    def test_one_class_stops_model(self):
        s=pd.DataFrame({'PositiveCashTax':[1]*60})
        _,_,info=fit_logit(s,pd.Series(True,index=s.index),['LogAssets'],'test')
        self.assertEqual(info['reason'],'INSUFFICIENT_SAMPLE_OR_OUTCOME_VARIATION')

if __name__=='__main__':
    unittest.main()
