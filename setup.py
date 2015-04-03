from IsirPythonTools import *

# try to find interesting module
eigen_lgsm             = pkgconfig("eigen_lgsm", True)

try:
    quadprog               = pkgconfig("quadprog", True)
except ValueError:
    print "Quadprog was not found, XDE-SwigISIRController and XDE-ISIRController will not be installed"
    print "Press Enter to continue"
    quadprog = None
    raw_input()

try:
    orc_framework          = pkgconfig("orc_framework", True)
except ValueError:
    print "orc_framework was not found, XDE-SwigISIRController and XDE-ISIRController will not be installed"
    print "Press Enter to continue"
    orc_framework = None
    raw_input()

try:
    orcisir_ISIRController = pkgconfig("orcisir_ISIRController", True)
except ValueError:
    print "orcisir_ISIRController was not found, XDE-SwigISIRController and XDE-ISIRController will not be installed"
    print "Press Enter to continue"
    orcisir_ISIRController = None
    raw_input()

try:
    isirtaskmanager = pkgconfig("isirtaskmanager", False)
except ValueError:
    print "isir_task_manager was not found will not be supported"
    print "Press Enter to continue"
    isir_task_manager = None
    raw_input()

try:
    xdecore                = pkgconfig("xdecore", True)
except ValueError:
    print "xdecore was not found, XDE-SwigISIRController and XDE-ISIRController will not be installed"
    print "Press Enter to continue"
    xdecore = None
    raw_input()

additional             = get_additional_include_dir_from_env()

orocos                 = pkgconfig("orocos-rtt-gnulinux", False)

# gather all data
other_swig_opt = []
other_compiler_args = []
packages_data_list = [eigen_lgsm]

if quadprog is not None:
    packages_data_list.append(quadprog)
if orc_framework is not None:
    packages_data_list.append(orc_framework)
if orcisir_ISIRController is not None:
    packages_data_list.append(orcisir_ISIRController)
if isirtaskmanager is not None:
    packages_data_list.append(isirtaskmanager)

packages_data_list.append(additional)

packages_data = get_packages_data(packages_data_list)


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


packages_dict={'xde_world_manager':'XDE-WorldManager/src',
              'xde_resources': 'XDE-Resources/src',
              'xde_robot_loader': 'XDE-RobotLoader/src',
              'xde_spacemouse': 'XDE-Spacemouse/src'}

package_data_dict={'xde_resources': ['resources/urdf/*.dae', 'resources/urdf/lwr/*.dae', 'resources/urdf/*.xml'],
                   'xde_robot_loader': ['simple_shapes.dae']}

ext_modules_list = []


#if Joseph's controller has been found, install XDE-SwigISIRController and XDE-ISIRController
if (orcisir_ISIRController and quadprog and orc_framework and xdecore) is not None:
    ext_modules_list = []
    # SwigISIRController
    _swig_swig_isir_controller = Extension("_swig_isir_controller",
                       ["XDE-SwigISIRController/src/swig_isir_controller.i"],
                       swig_opts = ["-c++"] + ["-I"+p for p in packages_data['include_dirs']] + other_swig_opt,
                       extra_compile_args = ["-fpermissive"] + other_compiler_args,
                       **packages_data #include, libs
                       )
    ext_modules_list.append(_swig_swig_isir_controller)

    if isirtaskmanager is not None:
        # isirtaskmanager
        _isir_task_manager = Extension("_isir_task_manager", 
                           ["XDE-SwigISIRController/src/isir_task_manager.i"],
                           swig_opts = ["-c++"] + ["-I"+p for p in packages_data['include_dirs']] + other_swig_opt,
                           extra_compile_args = ["-fpermissive"] + other_compiler_args,
                           **packages_data
                           )
        ext_modules_list.append(_isir_task_manager)


    #to force the package building extension before all we change the script_args list:
    import sys
    #sys.argv.remove("develop")
    script_args= ["build_ext", "--build-lib=XDE-SwigISIRController/src"] + sys.argv[1:] # To force a first build of the Extension(s)

    packages_dict['swig_isir_controller'] = 'XDE-SwigISIRController/src'
    packages_dict['xde_isir_controller'] = 'XDE-ISIRController/python/src'

    package_data_dict['swig_isir_controller'] = ['*.so']


setup(name='XDE-ISIR',
	  version='0.1',
	  description='',
	  author='Soseph',
	  author_email='hak@isir.upmc.fr',
      ext_modules = ext_modules_list,
	  package_dir = packages_dict,
	  packages = packages_dict.keys(),
      include_package_data=True,
	  package_data=package_data_dict,
	  cmdclass=cmdclass,

	  script_name=script_name,
	  script_args= script_args
	 )
