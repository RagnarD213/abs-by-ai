"""Regression checks for visible cuts, scaled tracking and native crop geometry."""
import ast
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[5]
spec=importlib.util.spec_from_file_location('landing',ROOT/'.claude/skills/_shared/cut/landing.py')
landing=importlib.util.module_from_spec(spec);spec.loader.exec_module(landing)

class VerticalLanding(unittest.TestCase):
    def test_scaled_cut_landing_and_speed(self):
        n=np.arange(240); raw=np.r_[900+np.arange(120)*.8,1200-np.arange(120)*.8]
        segments=[dict(n0=0,n1=120),dict(n0=120,n1=240)]
        for scale in [.5,1,2]:
            nn,x,heads,_=landing.vertical_dense(n,raw*scale,segments,608*scale,30)
            self.assertEqual(x[0],raw[0]*scale);self.assertEqual(x[120],raw[120]*scale)
            speed=np.abs(np.diff(x))*30
            self.assertLessEqual(max(np.r_[speed[:119],speed[120:]]),170*scale+1e-6)
            self.assertGreater(abs(x[-1]-raw[-1]*scale),1)
    def test_small_take_anchors_first_not_median(self):
        n=np.arange(60);raw=np.linspace(900,930,60)
        _,x,_=landing.vertical_track(n,raw,[dict(n0=0,n1=60)],608,30)
        np.testing.assert_equal(x,np.full(60,900))
    def test_missing_cut_measurement_fails(self):
        with self.assertRaisesRegex(ValueError,'cut frame 10'):
            landing.vertical_dense([0,7,14],[900,900,1200],[dict(n0=0,n1=10),dict(n0=10,n1=20)],608,30)
    def test_crop_map_preserves_height_and_reports(self):
        frames={i:[0,10,608,1080] for i in range(60)}
        stats=landing.vertical_crop_frames(frames,[dict(n0=0,n1=60)],np.arange(60),np.linspace(900,930,60),30)
        self.assertEqual(frames[0],[596,10,608,1080]);self.assertEqual(frames[59],frames[0])
        self.assertEqual(stats[0]['stats']['travel_px'],0)
    def test_window_expression_lands_on_new_take(self):
        # Execute the actual renderer function without running its historical build.
        file=ROOT/'.claude/skills/shortad-from-longform/reference/render.py'
        node=next(n for n in ast.parse(file.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='window_x_expr')
        ns=dict(np=np,json=json,os=os,__file__=str(file),FPS=30,_SPLICES=[2.],_seek_t=lambda t:t)
        exec(compile(ast.Module(body=[node],type_ignores=[]),str(file),'exec'),ns)
        current=Path.cwd()
        with tempfile.TemporaryDirectory() as tmp:
            os.chdir(tmp)
            try:
                raw=np.r_[np.linspace(900,925,60),np.linspace(1200,1175,60)]
                Path('facetrack_raw.json').write_text(json.dumps(dict(n=list(range(120)),x=raw.tolist())))
                expr=ns['window_x_expr'](0,4,608).replace('\\,',',')
                env=dict(clip=lambda x,a,b:min(max(x,a),b),gte=lambda x,y:float(x>=y))
                first=eval(expr,env,dict(t=0));cut=eval(expr,env,dict(t=2))
                self.assertAlmostEqual(first,596,places=5);self.assertAlmostEqual(cut,896,places=5)
                self.assertAlmostEqual(eval(expr,env,dict(t=59/30)),596,places=5)
            finally:os.chdir(current)

if __name__=='__main__':unittest.main()
