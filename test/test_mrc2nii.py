#
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
import pytools.ng.mrc2nifti
import pytest
import SimpleITK as sitk
import numpy as np

args = ["--help", "--version"]


@pytest.mark.parametrize("cli_args", args)
def test_mrc2nifti_main_help(cli_args):
    runner = CliRunner()
    result = runner.invoke(pytools.ng.mrc2nifti.main, cli_args.split())
    assert not result.exception


@pytest.mark.parametrize(
    "image_mrc,expected_pixel_type",
    [
        (sitk.sitkUInt8, sitk.sitkUInt8),
        (sitk.sitkInt16, sitk.sitkUInt16),
        (sitk.sitkUInt16, sitk.sitkUInt16),
        (sitk.sitkFloat32, sitk.sitkFloat32),
    ],
    indirect=["image_mrc"],
)
def test_mrc2nifti(image_mrc, expected_pixel_type):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(pytools.ng.mrc2nifti.main, [image_mrc, "out.nii"])
        assert not result.exception
        img = sitk.ReadImage("out.nii")

    assert img.GetPixelID() == expected_pixel_type
    assert img.GetSize() == (10, 9, 8)
    np.testing.assert_allclose(img.GetSpacing(), (1.1e-7, 1.2e-7, 1.3e-7))
