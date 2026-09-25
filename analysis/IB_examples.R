###
# Example Intentional Binding (IB) Calculation Script in R
# This script processes clock data (from import.R) to compute intentional binding effects as 
# defined by Haggard et al., (2002). # It checks for missing conditions and calculates IB effects 
# for subjects with complete data.
# author: @mcvinding
###

# Settings
use_condition2 <- FALSE    # Use wilcard conditions if available
min_trials <- 2           # Minimum number of trials per condition required for a subject to be included in the analysis

remove_outliers <- FALSE
max_cutoff <- 500         # ms
min_cutoff <- -500        # ms

# Input
datapath <- c('C:\\Users\\ncb623\\clock_test\\data')
infname <- file.path(datapath, paste0("combined_cleaned_data.csv"))
outfname <- file.path(datapath, paste0("ib_data_", Sys.Date(), ".csv"))

clock.data <- read.csv(infname, header=T)

#%% Check if all conditions are present for each subject
if (use_condition2) {
  condition_check <- expand.grid(id = unique(clock.data$id), condition1 = unique(clock.data$condition1), condition2 = unique(clock.data$condition2))
  condition_check$present <- paste(condition_check$id, condition_check$condition1, condition_check$condition2) %in% 
                             paste(clock.data$id, clock.data$condition1, clock.data$condition2)
} else {
  condition_check <- expand.grid(id = unique(clock.data$id), condition1 = unique(clock.data$condition1))
  condition_check$present <- paste(condition_check$id, condition_check$condition1) %in% 
                             paste(clock.data$id, clock.data$condition1)
}

# Report missing conditions
missing_conditions <- condition_check[!condition_check$present, ]
if (nrow(missing_conditions) > 0) {
  cat("Warning: Missing conditions found:\n")
  for (i in 1:nrow(missing_conditions)) {
    if (use_condition2) {
      cat(paste("Subject", missing_conditions$id[i], "missing condition:", missing_conditions$condition1[i], "+", missing_conditions$condition2[i], "\n"))
    } else {
      cat(paste("Subject", missing_conditions$id[i], "missing condition:", missing_conditions$condition1[i], "\n"))
    }
  }
} else {
  cat("All required conditions present for all subjects.\n")
}

# Fix NaNs in userError (for backwards compatibility)
clock.data$userError[is.na(clock.data$userError)] <- FALSE

# Remove errors and outliers (if relevant)
clock.data$shiftTime[clock.data$userError] <- NA 
if (remove_outliers==TRUE){
  extreme <- ifelse(clock.data$shiftTime > max_cutoff | clock.data$shiftTime < min_cutoff, T, F)         # Define outliers here (not recommended - always look at the data first!)
  clock.data$shiftTime[extreme] <- NA
  clock.data$outlier = extreme
}

# # Check which subjects have complete data for IB calculation
# complete_subjects <- aggregate(present ~ id, data = condition_check, FUN = all)
# incomplete_subjects <- complete_subjects$id[!complete_subjects$present]
# if (length(incomplete_subjects) > 0) {
#   cat("Subjects with incomplete data:", paste(incomplete_subjects, collapse = ", "), "\n")
# }

#%% Calculate summary statistics
if (use_condition2) {
  # Create complete grid of all id-condition1-condition2 combinations
  full_grid <- expand.grid(id = unique(clock.data$id), 
                           condition1 = unique(clock.data$condition1),
                           condition2 = unique(clock.data$condition2))
  
  # Aggregate only for combinations that exist
  agg.data <- aggregate(shiftTime ~ id + condition1 + condition2, data=clock.data, FUN=mean, na.rm=T)
  colnames(agg.data)[which(names(agg.data) == "shiftTime")] <- "meanShiftTime"
  agg.data$sd <- aggregate(shiftTime ~ id + condition1 + condition2, data=clock.data, FUN=sd, na.rm=T)[,4]
  agg.data$nTrials <- aggregate(shiftTime ~ id + condition1 + condition2, data=clock.data, FUN=function(x) sum(!is.na(x)))[,4]
  
  # Merge back to full grid, keeping all combinations with NA/0 for missing
  agg.data <- merge(full_grid, agg.data, by=c("id", "condition1", "condition2"), all.x=TRUE)
  agg.data$nTrials[is.na(agg.data$nTrials)] <- 0

} else {
  # Create complete grid of all id-condition1 combinations
  full_grid <- expand.grid(id = unique(clock.data$id), 
                           condition1 = unique(clock.data$condition1))
  
  # Aggregate only for combinations that exist
  agg.data <- aggregate(shiftTime ~ id + condition1, data=clock.data, FUN=mean, na.rm=T)
  colnames(agg.data)[which(names(agg.data) == "shiftTime")] <- "meanShiftTime"
  agg.data$sd <- aggregate(shiftTime ~ id + condition1, data=clock.data, FUN=sd, na.rm=T)[,3]
  agg.data$nTrials <- aggregate(shiftTime ~ id + condition1, data=clock.data, FUN=function(x) sum(!is.na(x)))[,3]
  
  # Merge back to full grid, keeping all combinations with NA/0 for missing
  agg.data <- merge(full_grid, agg.data, by=c("id", "condition1"), all.x=TRUE)
  agg.data$nTrials[is.na(agg.data$nTrials)] <- 0
}

agg.data <- agg.data[order(agg.data$id),]

# Flag conditions that meet minimum trials requirement
agg.data$include <- agg.data$nTrials >= min_trials
n_excluded <- sum(!agg.data$include)
if (n_excluded > 0) {
  cat("Flagged", n_excluded, "condition(s) as excluded due to fewer than", min_trials, "trials\n")
}

#%% Calculate intentional binding (IB) effects
# Loop through each subject
ib.data <- data.frame()
for (subj in unique(agg.data$id)) {
  if (use_condition2) {
    sub.dat <- data.frame(id=subj, condition = unique(agg.data$condition2), IB.press = NA, IB.tone = NA)

    # Get all conditions for this subject
    for (cond in unique(agg.data$condition2)) {
      tmp.dat <- subset(agg.data, id == subj & condition2 == cond)

      # Calculate IB.press: IB-press minus IB-singlePress
      if (tmp.dat[tmp.dat$condition1 == "IB-press", "include"] & tmp.dat[tmp.dat$condition1 == "IB-singlePress", "include"]) {
        press_val <- tmp.dat[tmp.dat$condition1 == "IB-press", "meanShiftTime"]
        single_press_val <- tmp.dat[tmp.dat$condition1 == "IB-singlePress", "meanShiftTime"]
        sub.dat[sub.dat$id == subj & sub.dat$condition == cond, "IB.press"] <- press_val - single_press_val
      }
      # Calculate IB.tone: IB-tone minus IB-singleTone
      if (tmp.dat[tmp.dat$condition1=="IB-tone", "include"] & tmp.dat[tmp.dat$condition1 == "IB-singleTone", "include"]) {
        tone_val <- tmp.dat[tmp.dat$condition1 == "IB-tone", "meanShiftTime"]
        single_tone_val <- tmp.dat[tmp.dat$condition1=="IB-singleTone", "meanShiftTime"]
        sub.dat[sub.dat$id == subj & sub.dat$condition==cond, "IB.tone"] <- tone_val - single_tone_val
      }
    }
    ib.data <- rbind(ib.data, sub.dat)
  } else {
    sub.dat <- data.frame(id=subj, IB.press=NA, IB.tone=NA)
    tmp.dat <- subset(agg.data, id == subj)

    if(tmp.dat[tmp.dat$condition1 == "IB-press", "include"] & tmp.dat[tmp.dat$condition1 == "IB-singlePress", "include"]) {
        press_val <- tmp.dat[tmp.dat$condition1 == "IB-press", "meanShiftTime"]
        single_press_val <- tmp.dat[tmp.dat$condition1 == "IB-singlePress", "meanShiftTime"]
        sub.dat[sub.dat$id == subj, "IB.press"] <- press_val - single_press_val
      }
      # Calculate IB.tone: IB-tone minus IB-singleTone
      if (tmp.dat[tmp.dat$condition1=="IB-tone", "include"] & tmp.dat[tmp.dat$condition1 == "IB-singleTone", "include"]) {
        tone_val <- tmp.dat[tmp.dat$condition1 == "IB-tone", "meanShiftTime"]
        single_tone_val <- tmp.dat[tmp.dat$condition1=="IB-singleTone", "meanShiftTime"]
        sub.dat[sub.dat$id == subj, "IB.tone"] <- tone_val - single_tone_val
      }

    ib.data <- rbind(ib.data, sub.dat)
  }
}

## SAVE DATA
write.csv(ib.data, file="ib_data.csv", row.names=FALSE)
