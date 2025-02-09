#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0.txt
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from click.testing import CliRunner
import pytools.ng.mrc2ngpc
import pytest
import SimpleITK as sitk
import json

args = ["--help", "--version"]


@pytest.mark.parametrize("cli_args", args)
def test_mrc2ngpc_main_help(cli_args):
    runner = CliRunner()
    result = runner.invoke(pytools.ng.mrc2ngpc.main, cli_args.split())
    assert not result.exception


@pytest.mark.parametrize(
    "image_mrc,expected_pixel_type",
    [
        (sitk.sitkUInt8, sitk.sitkUInt8),
        (sitk.sitkInt16, sitk.sitkUInt16),
        (sitk.sitkUInt16, sitk.sitkUInt16),
    ],
    indirect=["image_mrc"],
)
def test_mrc2ngpc(image_mrc, expected_pixel_type):
    runner = CliRunner()
    ng_path = "output_ngpc"
    with runner.isolated_filesystem():
        result = runner.invoke(pytools.ng.mrc2ngpc.main, [image_mrc, ng_path])
        assert not result.exception

        with open("mrc2ngpc-output.json") as fp:
            mm = json.load(fp)
            assert "neuroglancerPrecomputedMin" in mm
            assert "neuroglancerPrecomputedMin" in mm
            assert "neuroglancerPrecomputedFloor" in mm
            assert "neuroglancerPrecomputedLimit" in mm
            assert type(mm["neuroglancerPrecomputedMin"]) == str
            assert type(mm["neuroglancerPrecomputedMax"]) == str
            assert type(mm["neuroglancerPrecomputedFloor"]) == str
            assert type(mm["neuroglancerPrecomputedLimit"]) == str
