include_directories(
"${CMAKE_SOURCE_DIR}/scribus"
)

install(FILES
ISOcoated_v2_300_bas.icc
ISOcoated_v2_300_bas.txt
Readme
sRGB_icc22.icm
sRGB_icc22.txt
  DESTINATION ${SHAREDIR}profiles
)
