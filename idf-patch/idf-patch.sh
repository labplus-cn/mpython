

echo "Begin patch."

echo $IDF_PATH

if [ $IDF_PATH ]; then 
    cp idf_patch.patch $IDF_PATH/idf-patch.patch
    cd $IDF_PATH
    git apply idf-patch.patch
    echo "patch end."
else 
    echo   "Please set IDF_PATH environment variable." 
fi

