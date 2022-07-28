# **************************************************************************
# *                                                                        *
# *  Copyright (C) Golaem S.A.  All Rights Reserved.                       *
# *                                                                        *
# **************************************************************************

# **************************************************************************
#! \file Golaem Utils
#  \brief Golaem functions with no dependencies from Maya!!
# **************************************************************************

# DO NOT ADD ANY MAYA DEPENDENCY HERE
from builtins import str
from builtins import range
import re
import sys

# DO NOT ADD ANY MAYA DEPENDENCY HERE

usingDevkit = True
try:
    import glm.devkit as devkit
except:
    usingDevkit = False

# ------------------------------------------------------------
def convertStringForDevkit(value):
    if sys.version_info.major >= 3:
        return str(value)
    return value.encode()


# **************************************************************************
#! @name File Utils
# **************************************************************************
# @{
# ------------------------------------------------------------
#! Return the file path prefix of an exported file (same as getExportedFilePath but without the frame and the extension)
#! \note: ends with a "."
# ------------------------------------------------------------
def getExportedFilePrefix(directory, cacheName, crowdField):
    if usingDevkit:
        directory = devkit.replaceEnvVars(convertStringForDevkit(directory))
    return directory + "/" + cacheName + "." + convertToValidName(crowdField) + "."


# ------------------------------------------------------------
#! Return the simulation cache file path
# ------------------------------------------------------------
def getSimulationCachePath(cachePrefix, frame):
    return cachePrefix + str(frame) + ".gscf"


# ------------------------------------------------------------
#! Convert a str (such as a nodeName) to a a valid str for file naming
#  \str str to convert
# ------------------------------------------------------------
def convertToValidName(str):
    validStr = list(str)

    # check first letter
    if validStr[0] == "0":
        validStr[0] = "a"
    elif validStr[0] == "1":
        validStr[0] = "b"
    elif validStr[0] == "2":
        validStr[0] = "c"
    elif validStr[0] == "3":
        validStr[0] = "d"
    elif validStr[0] == "4":
        validStr[0] = "e"
    elif validStr[0] == "5":
        validStr[0] = "f"
    elif validStr[0] == "6":
        validStr[0] = "g"
    elif validStr[0] == "7":
        validStr[0] = "h"
    elif validStr[0] == "8":
        validStr[0] = "i"
    elif validStr[0] == "9":
        validStr[0] = "j"

    # replace special characters with _ or __
    expr = re.compile("[a-zA-Z0-9|@]")
    for iS in range(1, len(validStr)):
        if expr.match(validStr[iS]) is None:
            if validStr[iS] == ":":
                validStr.insert(iS + 1, "_")
            validStr[iS] = "_"
    return "".join(validStr)


# @}

