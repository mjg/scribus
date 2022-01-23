#! /bin/sh

if [ -z "$1" ]; then
    echo "no version specified, assuming checkout"
else
    version=$1
    nv=scribus-${version}

    archive=${nv}.tar.xz
    freearchive=${nv}-free.tar.xz

    echo "Verify if source available. Download may be needed"
[ -f ${archive} ] || curl -OL http://downloads.sourceforge.net/scribus/scribus-${version}.tar.xz

    echo "Extracting sources ..."
    rm -rf ${nv}
    tar -xJf $archive

    pushd ${nv}
fi

# remove docs
rm -r doc
sed -i '/add_subdirectory(doc)/d' CMakeLists.txt
echo "doc folder removed"

# remove non-free profiles
rm resources/profiles/{GenericCMYK.icm,GenericCMYK.txt,sRGB.icm,srgb.license}
sed -i '/GenericCMYK/d' resources/profiles/CMakeLists.txt
sed -i '/sRGB.icm/d' resources/profiles/CMakeLists.txt
sed -i '/srgb.license/d' resources/profiles/CMakeLists.txt
echo "Non-free profiles removed"

# remove non-free swatches
rm resources/swatches/Galaxy_*
rm resources/swatches/Resene_*
rm resources/swatches/Federal_Identity_Program.xml
echo "Non-free swatches removed"

# Remove non-free (CC-BY-SA-NC) dot files
rm resources/editorconfig/dot.*
sed -i '/dot.svg/d' resources/editorconfig/CMakeLists.txt
echo "Non-free dot files removed"

# Remove non-free dicts files
rm -r resources/dicts
sed -i '/dicts/d' CMakeLists.txt
echo "Non-free dicts removed"

if [ -n "$1" ]; then
    popd

    echo "Creating sources ..."
    tar cf - ${nv} | xz > ${freearchive}
    echo "Source free archives created"
fi
echo "Task completed"
