'''
Import clock-test data from raw experiment output files.

'''
#%%##################################################################################################
# Set working directory to the folder where the data files are located
datapath <- c('C:\\Users\\ncb623\\clock_test\\data')

# Specify subjects and conditions to be imported
subjects <- c('666')                                              # Write the subject numbers here
conditions <- c("IB-press","IB-tone","IB-singlePress","IB-singleTone")   # Write the names of the conditions here

#%%##################################################################################################
# Settings
clockspeed <- 2650          # Speed of the clock in ms per full rotation (2550ms in original Libet clock test)
EMGdelay <- 65              # Average delay of EMG onset after button press (65 ms)

#%%##################################################################################################
# Import clock test data
setwd(datapath)

all.files <- sort(list.files(datapath))
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

  temp.dat <- temp.dat[,-(11:15)]    # Remove unnecessary columns (for now)
    
  # Recalculate angles and errors
  recalc.1 <- ifelse(temp.dat$ansAngle < 100 & temp.dat$pressAngle > 270,T,F)
  temp.dat$ansAngle[recalc.1] <- temp.dat$ansAngle[recalc.1]+360               # +1,+H
  recalc.2 <- ifelse(temp.dat$ansAngle>260 & temp.dat$pressAngle<100,T,F)
  temp.dat$pressAngle[recalc.2] <- temp.dat$pressAngle[recalc.2]+360           # +H,+1    
  temp.dat$recalc <- recalc.1 | recalc.2
 
  temp.dat$errAngle <- temp.dat$ansAngle-temp.dat$pressAngle
  temp.dat$errTime <- temp.dat$errAngle*clockspeed/360            # Convert angle error to time error (ms) based on 2550ms rotation time
  # errTimeEMG <- errTime+EMGdelay
  
  # Fix datatypes
  temp.dat$id <- as.factor(temp.dat$id)
  temp.dat$condition <- as.factor(temp.dat$condition)

  # Create clean condition variable - remove trailing numbers only if they exist
  temp.dat$condition_clean <- gsub("\\d+$", "", as.character(temp.dat$condition))
  # Match against the predefined conditions list to ensure consistency
  for (i in 1:length(conditions)) {
    temp.dat$condition_clean[grepl(paste0("^", conditions[i]), temp.dat$condition_clean)] <- conditions[i]
  }
  temp.dat$condition_clean <- as.factor(temp.dat$condition_clean)
  
  # Remove errors and outliers 
#     extreme <- ifelse(errorTime > 500 | errorTime < -500,T,F)         # Define outliers here (not recommended - always look at the data first!)
  errors <- as.logical(temp.dat$userError) #| extreme
  # errTime[errors] <- NA
  # errTimeEMG[errors] <- NA

  clock.data <- rbind(clock.data, temp.dat)
}

#%% Save data

# END