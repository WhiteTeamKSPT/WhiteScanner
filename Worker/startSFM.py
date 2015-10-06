import subprocess

def startSFM(options, input_dir, output_file):
    """
    Starts VisualSFM with input parameters
    VisualSFM sfm[options] input output.nvm [user_data_path]

    options = [match_option][sfm_option][misc_option][mvs_option]

    match_option = [+pairs/+import/+subset/+nomatch/]
        +pairs:   match image pairs from [user_data_path];
        +import:  load feature matches from [user_data_path];
        +subset:  match a prioritized subset of pairs when
                  #images >= param_prioritized_subset_switch;
        +nomatch: reconstruction without feature matching;
        default:  compute missing pairwise matches.

    sfm_option = [+resume/+add/+skipsfm/+loadnvm/]
        +resume:  load NVM file, try add new images from
                  [input].txt, and grow the existing models;
        +add:     load NVM file, and find more points and
                  projections for the existing models;
        +loadnvm: load NVM file and skip feature matching;
        +skipsfm: skip sparse and dense reconstruction;
        default:  run regular sparse reconstruction.

    misc_option = [+k=fx,cx,fy,cy/+shared][+sort][+gcp]
        +k:       fixed calibration, e.g. +k=1024,800,1024,600;
        +shared:  enforce shared calibration in the end;
        +sort:    keep the input image order in the output NVM;
        +gcp:     load GCPs from [input].gcp and transform the 3D model.

    mvs_option = [+pmvs/+cmvs/+cmp/]
        +cmvs:    undistort images, run CMVS/genOption, skip PMVS;
        +pmvs:    undistort images, run CMVS/genOption/PMVS;
        +cmp:     undistort images, write p-matrices for CMP-MVS;
        default:  skip the entire dense reconstruction.
    <output.nvm> is where reconstruction is saved
    Examples:
    VisualSFM sfm ../my_jpg_folder ../results/my_result.nvm //sparse reconstruction from folder
    VisualSFM sfm+pmvs my_jpg_list.txt my_result.nvm        //sparse+dense from image list
    VisualSFM sfm+resume initial.nvm final.nvm              //resume sparse reconstruction
    VisualSFM sfm+pairs input output.nvm my_pairs.txt       //use [my_pairs] for matching, and run sfm
    VisualSFM sfm+pairs input output.nvm @10                //matching pairs within 10, and run sfm
    VisualSFM sfm+import input output.nvm my_matches.txt    //load [my_matches], and run sfm
    VisualSFM sfm+loadnvm+pmvs sparse.nvm  dense.nvm        //open NVM and run dense reconstruction
    VisualSFM sfm+loadnvm+cmvs input.nvm export.nvm         //open NVM and export PMVS data
    """
    cmd = './VisualSFM ' + str(options) +  ' ' + str(input_dir) + ' ' + str(output_file)

    PIPE = subprocess.PIPE
    p = subprocess.call(cmd, shell = True)
