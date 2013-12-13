from IsirPythonTools import *

# try to find interesting module
eigen_lgsm             = pkgconfig("eigen_lgsm", True)
quadprog               = pkgconfig("quadprog", True)
orc_framework          = pkgconfig("orc_framework", True)
orcisir_ISIRController = pkgconfig("orcisir_ISIRController", True)
xdecore                = pkgconfig("xdecore", False)
additional             = get_additional_include_dir_from_env()

orocos                 = pkgconfig("orocos-rtt-gnulinux", False)

# gather all data
other_swig_opt = []
other_compiler_args = []
packages_data = get_packages_data([eigen_lgsm, quadprog, orc_framework, orcisir_ISIRController, additional])


# check for optional package: xde
if xdecore is not None:
    xde_data = get_packages_data([xdecore])
    for elem in ["include_dirs", "library_dirs", "libraries"]:
        packages_data[elem].extend(xde_data[elem])
    other_swig_opt.append("-DXDECORE_IS_AVAILABLE")


# check for optional package: orocos
if orocos is not None:
    incdir = commands.getoutput("pkg-config --variable=includedir orocos-rtt-gnulinux")
    libdir = commands.getoutput("pkg-config --variable=libdir orocos-rtt-gnulinux")
    packages_data["include_dirs"].extend([incdir, incdir+os.sep+"rtt"])
    packages_data["library_dirs"].extend([libdir])
    packages_data["libraries"].extend(["orocos-rtt-gnulinux"])
    other_compiler_args.extend(["-DOROCOS_TARGET=gnulinux"])
    other_swig_opt.append("-DOROCOS_IS_AVAILABLE")



# SwigISIRController
_swig_swig_isir_controller = Extension("_swig_isir_controller",
                   ["XDE-SwigISIRController/src/swig_isir_controller.i"],
                   swig_opts = ["-c++"] + ["-I"+p for p in packages_data['include_dirs']] + other_swig_opt,
                   extra_compile_args = ["-fpermissive"] + other_compiler_args,
                   **packages_data #include, libs
                   )



#to force the package building extension before all we change the script_args list:
import sys
#sys.argv.remove("develop")
script_args= ["build_ext", "--build-lib=XDE-SwigISIRController/src"] + sys.argv[1:] # To force a first build of the Extension(s)

packages_dict={'xde_world_manager':'XDE-WorldManager/src',
              'xde_resources': 'XDE-Resources/src',
              'xde_robot_loader': 'XDE-RobotLoader/src',
              'xde_spacemouse': 'XDE-Spacemouse/src',
              'swig_isir_controller': 'XDE-SwigISIRController/src',
              'xde_isir_controller': 'XDE-ISIRController/src'}

setup(name='XDE-ISIR',
	  version='0.1',
	  description='',
	  author='Soseph',
	  author_email='hak@isir.upmc.fr',
      ext_modules = [_swig_swig_isir_controller],
	  package_dir = packages_dict,
	  packages = packages_dict.keys(),
      include_package_data=True,
	  package_data={'xde_resources': ['resources/urdf/*.dae', 'resources/urdf/lwr/*.dae', 'resources/urdf/*.xml'],
                    'swig_isir_controller':['*.so']},
	  cmdclass=cmdclass,

	  script_name=script_name,
	  script_args= script_args
	 )
