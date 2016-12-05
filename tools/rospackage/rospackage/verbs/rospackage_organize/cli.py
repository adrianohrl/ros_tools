from __future__ import print_function

from osrf_pycommon.terminal_color import print_color

from rospkg import ResourceNotFound

from rospackage.common import Package
from rospackage.common import create
from rospackage.common import locate
from rospackage.common import move

def prepare_arguments(parser):
    parser.description="This verb is used to organize ROS packages, gathering the\
        EXTENSION(s) files into their respective FOLDER. If a EXTENSION file is\
        found out of its proper FOLDER, it will be replaced to there. Calling\
        'rospackage organize' with no arguments after the PACKAGE(s) specification\
        will execute as '--all' argument."
    parser.add_argument('-p', '--packages', type=str, nargs='+',
        dest='packages', metavar='PACKAGE', required=True,
        help='specify the ROS package in which this operation will be done.'
    )
    parser.add_argument('-a', '--all', action='store_true', 
        help='gather all the .CONFIG, .MACHINE, .RVIZ, .URDF, .XACRO, and .YAML files of the\
            PACKAGE into the CONFIG folder (if necessary, it is created); as well as, gather\
            all the .ACTION, .BAG, .LAUNCH, .MAP, .MMSG, .MSG, and .SRV files into their\
            respective folder (whose name is equal to their files extension).'
    )
    parser.add_argument('-e', '--extension', action='append', type=str, nargs='+',
        #choices=['action','bag','config','launch','machine',map','mmsg','msg','srv','rviz','urdf','xacro','yaml'], 
        dest='extensions', metavar='EXTENSION', default=list(),
        help='specify the EXTENSION(s) files to be gathered into a FOLDER. If FOLDER is not'
            'given, the EXTENSION(s) files will be replaced to a folder whose name is equal'
            'to the EXTENSION of their inner files.'
    )
    parser.add_argument('-f', '--folder', action='append', type=str,  
        dest='folders', metavar='FOLDER', default=list(),
        help='specify the FOLDER in which the EXTENSION(s) files will to replaced to (if needed).'
    )
    parser.add_argument('-q', '--quiet', action='store_true',
        help='quiet info, warning and error messages.'
    )
    return parser


def main(options):

    if options.all or len(options.extensions) == 0:
        options.extensions = list()
        options.extensions.append(['conf', 'machine', 'perpective', 'rviz', 'urdf', 'xacro', 'yaml'])
        options.folders = list()
        options.folders.append('config')
        options.extensions.append(['action', 'bag', 'launch', 'map', 'mmsg', 'msg', 'srv'])

    report = not options.quiet
    packages = list()
    for package_name in options.packages:
        try:
            package = Package(package_name)
        except ResourceNotFound:
            if report: 
                print_color("@{red}[ERROR] %s is not a ROS package." % package_name)
            continue
        for i in range(len(options.extensions)):
            if i < len(options.folders):
                folder_name = options.folders[i];
            for folder_extension in options.extensions[i]:
                if folder_extension.startswith("."):
                    if report:
                        print_color("@{red}[ERROR] The extension names must be entered with not dot.")
                    continue
                    folder_extension = folder_extension
                if i >= len(options.folders):
                    folder_name = folder_extension
                package.extensions["." + folder_extension] = folder_name
        if len(package.extensions) == 0:
            if report: 
                print_color("@{red}[ERROR] None folder.")
            return 1
        organize(package, report)
        packages.append(package)

    if not packages:
        if report: 
            print_color("@{red}[ERROR] None valid ROS package.")
        return 1

    if report:
        print_color("\n@!@{green}==>@|@! Reporting...")
        print_color("packages:")
        for package in packages:
            print_color("%s" % package.pretty())
        print_color("End of report.\n")

    return 0


def organize(package, report):
    if report:
        print_color("@!@{green}==>@|@! Processing %s package..." % package.name)
    for extension, folder_name in package.extensions.items():
        files = locate(package, extension, package.path)
        if not files:
            if report:
                print_color("@{yellow}[WARN] None %s file was found in the %s package." % (extension.upper(), package.name))
        else:
            if not package.files_to_be_moved:
                if report:
                    print_color("[INFO] All %s file is located at their proper folder (%s) in the %s package." % (extension.upper(), folder_name, package.name))
            else:
                folder = create(folder_name, package, report)   
                for file in package.files_to_be_moved:
                    move(file, folder, package, report)
                package.clear()
        del files[:]
    for folder in package.folders:
        if folder.isEmpty():
            package.remove(folder.name)