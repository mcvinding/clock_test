###
# Import clock-test data from raw experiment output files.
# author: @mcvinding
###

#%%##################################################################################################
# Set working directory to the folder where the data files are located
datapath <- c('C:\\Users\\ncb623\\clock_test')

# Specify subjects and conditions to be imported
subjects <- c('333', '666')                                              # Write the subject numbers here
conditions <- c("IB-press","IB-tone","IB-singlePress","IB-singleTone")   # Write the names of the conditions here

wildcard_keys <- c('Self', 'Other')

raw.path <- file.path(datapath, 'raw_data')
out.path <- file.path(datapath, 'data')

#%%##################################################################################################
# Settings
clockspeed <- 2650          # Speed of the clock in ms per full rotation (2550ms in original Libet clock test)
# EMGdelay <- 65              # Average delay of EMG onset after button press (65 ms)

outfname <- file.path(out.path, paste0("combined_cleaned_data_", Sys.Date(), ".csv"))
#%%##################################################################################################
# Import clock test data
setwd(raw.path)

all.files <- sort(list.files(raw.path))
in.files <- all.files[grepl(paste(subjects, collapse="|"), all.files) & grepl(paste(conditions, collapse="|"), all.files)]
sub.data <- data.frame()
clock.data <- data.frame()

for (ff in in.files){
  print(paste("Importing file:",ff))
  temp.dat <- read.csv(ff, sep=";",header=T)

  # Check if file is empty (no data rows)
  if (nrow(temp.dat) == 0) {
    print(paste("Warning: File is empty, skipping:", ff))
    next
  }

  # temp.dat <- temp.dat[,-(11:15)]    # Remove unnecessary columns (for now)

  # Recalculate angles and "errors"
  if(grepl('tone', ff, ignore.case=TRUE)) {    recalc.1 <- ifelse(temp.dat$ansAngle < 100 & temp.dat$toneAngle > 270,T,F)
    recalc.1[is.na(recalc.1)] <- FALSE
    temp.dat$ansAngle[recalc.1] <- temp.dat$ansAngle[recalc.1]+360               # +1,+H

    recalc.2 <- ifelse(temp.dat$ansAngle>260 & temp.dat$toneAngle<100,T,F)
    recalc.2[is.na(recalc.2)] <- FALSE
    temp.dat$toneAngle[recalc.2] <- temp.dat$toneAngle[recalc.2]+360           # +H,+1    

    temp.dat$recalc <- recalc.1 | recalc.2
    temp.dat$shiftAngle <- temp.dat$ansAngle-temp.dat$toneAngle
  } else {
    recalc.1 <- ifelse(temp.dat$ansAngle < 100 & temp.dat$pressAngle > 270,T,F)
    recalc.1[is.na(recalc.1)] <- FALSE
    temp.dat$ansAngle[recalc.1] <- temp.dat$ansAngle[recalc.1]+360               # +1,+H

    recalc.2 <- ifelse(temp.dat$ansAngle>260 & temp.dat$pressAngle<100,T,F)
    recalc.2[is.na(recalc.2)] <- FALSE
    temp.dat$pressAngle[recalc.2] <- temp.dat$pressAngle[recalc.2]+360           # +H,+1    

    temp.dat$recalc <- recalc.1 | recalc.2
    temp.dat$shiftAngle <- temp.dat$ansAngle-temp.dat$pressAngle
  }

  temp.dat$shiftTime <- temp.dat$shiftAngle*clockspeed/360            # Convert angle error to time error (ms) based on rotation time
  # errTimeEMG <- temp.dat$errTime + EMGdelay
  
  # Extract wildcard key if it exists in the condition
  temp.dat$condition2 <- NA_character_
  for (wc in wildcard_keys) {
    temp.dat$condition2[grepl(wc, temp.dat$condition)] <- wc
  }
  
  # Create clean condition variable - remove trailing numbers only if they exist
  temp.dat$condition1 <- gsub("\\d+$", "", as.character(temp.dat$condition))
  # Match against the predefined conditions list to ensure consistency
  for (i in 1:length(conditions)) {
    temp.dat$condition1[grepl(paste0("^", conditions[i]), temp.dat$condition1)] <- conditions[i]
  }
  
  # Fix datatypes
  temp.dat$id <- as.factor(temp.dat$id)
  temp.dat$condition <- as.factor(temp.dat$condition)
  temp.dat$condition1 <- as.factor(temp.dat$condition1)
  temp.dat$condition2 <- as.factor(temp.dat$condition2)
  temp.dat$userError <- as.logical(temp.dat$userError)
  
  # Combine data
  clock.data <- rbind(clock.data, temp.dat)
}

#%% Save data
if (!dir.exists(out.path)) {
  dir.create(out.path)
}

write.csv(clock.data, file=outfname, row.names=FALSE)

# END