#!/bin/bash

# This is only an example file. How you create your package is not important, do it as you please.
# Every package build itself. This is different that, for example, deb or rpm. We do this since
# in MilkyWhite, the steps before the building are more important then the result, which is a 
# stupid simple tar.bz2 file
# Normally, a project that needs MilkyWhite needs a lot of preparation on deploy, like joining
# and compressing static files (css, js), generating static cache files and so on. 
# After that, creating a zip file is not really the complex part of it. 


# In a real-live situation, the version would be dynamic and given by paramter or taken from a
# VCS like subversion or git.
rm -f ../testpackage_version1.tar.bz2
tar -jcf ../testpackage_version1.tar.bz2 .
