# -*- coding: utf-8 -*-

# The purpose of this script is to read the .env.dist file and create the .env file
# required for launching Docker. The values are pulled from environnement variables
# set by Travis

import os

final_env_file = open('.env', 'w')
dist_env_file = open('.env.dist', 'r')

# Process each variables in the dist file
for line in dist_env_file.readlines():
    # Ignore blank and comment lines
    if (line.strip() != '' and not line.startswith('#')):
        variable_name = line.split('=')[0]
        variable_value = os.getenv(variable_name, '')
        final_env_file.write(variable_name + "=" + variable_value + "\n")

final_env_file.close()
dist_env_file.close()
