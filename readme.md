
# Using Conda
conda create -n ir python=3.9 
# Setup of Environment
conda activate ir
pip install -r requirements.txt
python init.py


# To run the program 
## Preparation of Document Collection and stop word Removal
python my_ir_system.py —-extract-collection aesop10.txt

## Linear Search through the document
Example for searching query wolf with model bool and searchmode linear within original documents only:
python my_ir_system.py --query "wolf" --model "bool" --search-mode "linear" --documents "original"
