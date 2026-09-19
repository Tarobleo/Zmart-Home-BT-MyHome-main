"""Regression checks for nested device-schema post-processing.

Run with Python, voluptuous and PyYAML; Home Assistant constants are stubbed.
"""
import ast
import copy
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import voluptuous as vol
import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_validator():
    scope = {}
    exec((ROOT / 'custom_components/myhome/const.py').read_text(), scope)
    scope.update(CONF_NAME='name', CONF_MAC='mac')
    for platform in ('light', 'switch', 'cover', 'button', 'sensor', 'binary_sensor', 'climate'):
        scope[platform.upper()] = platform
    tree = ast.parse((ROOT / 'custom_components/myhome/validate.py').read_text())
    for cls in ('SwitchDeviceClass', 'SensorDeviceClass', 'BinarySensorDeviceClass'):
        attrs = {n.attr: n.attr.lower() for n in ast.walk(tree)
                 if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == cls}
        scope[cls] = SimpleNamespace(**attrs)
    scope['ha_format_mac'] = lambda value: ':'.join(value[i:i+2] for i in range(0, 12, 2)).lower()
    tree.body = [n for n in tree.body if not isinstance(n, ast.ImportFrom)
                 or n.module == 'voluptuous']
    exec(compile(tree, 'validate.py', 'exec'), scope)
    return scope['config_schema']


class ConfigNormalizationTest(unittest.TestCase):
    def check_config(self):
        validate = load_validator()
        raw = yaml.safe_load((ROOT / 'myhome-all-identified.yaml').read_text())
        result = validate(copy.deepcopy(raw))
        platforms = result['00:00:00:00:00:00']['platforms']
        for platform in ('light', 'cover'):
            self.assertTrue(platforms[platform])
            for key, device in platforms[platform].items():
                self.assertEqual(key, f"{device['who']}-{device['where']}")
                for field in ('icon', 'icon_on', 'entity_name', 'entities'):
                    self.assertIn(field, device)
                self.assertIs(platforms['button'][key], device)
        self.assertIn('1-0402', platforms['light'])
        raw = {'gateway': {'mac': '00:00:00:00:00:00',
                          'climate': {'zone': {'zone': '3', 'central': True}},
                          'sensor': {'meter': {'where': '51', 'name': 'Meter', 'class': 'power'}}}}
        platforms = validate(raw)['00:00:00:00:00:00']['platforms']
        self.assertEqual(platforms['climate']['4-3']['zone'], '#0#3')
        self.assertIn('entities', platforms['sensor']['18-51'])
        with self.assertRaises(vol.Invalid):
            validate({'gateway': {'mac': 'invalid'}})

    def test_standard_compiler(self):
        self.check_config()

    def test_compiler_inlining_nested_schemas(self):
        original = vol.Schema._compile
        def inline(schema_self, schema):
            if isinstance(schema, vol.Schema):
                return schema._compiled
            return original(schema_self, schema)
        with patch.object(vol.Schema, '_compile', inline):
            self.check_config()


if __name__ == '__main__':
    unittest.main()
