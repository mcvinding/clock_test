'''
# Example Intentional Binding (IB) Calculation Script in R
# This script processes clock data (from import.R) to compute intentional binding effects as defined by Haggard et al., 2002.
# It checks for missing conditions and calculates IB effects for subjects with complete data.
author: @mc_vinding
'''

#%% Check if all conditions are present for each subject
condition_check <- expand.grid(id = unique(clock.data$id), condition_clean = conditions)
condition_check$present <- paste(condition_check$id, condition_check$condition_clean) %in% 
                           paste(clock.data$id, clock.data$condition_clean)

# Report missing conditions
missing_conditions <- condition_check[!condition_check$present, ]
if (nrow(missing_conditions) > 0) {
  cat("Warning: Missing conditions found:\n")
  for (i in 1:nrow(missing_conditions)) {
    cat(paste("Subject", missing_conditions$id[i], "missing condition:", missing_conditions$condition_clean[i], "\n"))
  }
} else {
  cat("All required conditions present for all subjects.\n")
}

# Check which subjects have complete data for IB calculation
complete_subjects <- aggregate(present ~ id, data = condition_check, FUN = all)
incomplete_subjects <- complete_subjects$id[!complete_subjects$present]
if (length(incomplete_subjects) > 0) {
  cat("Subjects with incomplete data (cannot calculate IB):", paste(incomplete_subjects, collapse = ", "), "\n")
}

#%% Calculate summary statistics
agg.data <- aggregate(errTime ~ id + condition_clean, data=clock.data, FUN=mean, na.rm=T)
colnames(agg.data)[which(names(agg.data) == "errTime")] <- "meanErrTime"
agg.data$sdErrTime <- aggregate(errTime ~ id + condition_clean, data=clock.data, FUN=sd, na.rm=T)[,3]
agg.data$nTrials <- aggregate(errTime ~ id + condition_clean, data=clock.data, FUN=function(x) sum(!is.na(x)))[,3]
agg.data$seErrTime <- agg.data$sdErrTime / sqrt(agg.data$nTrials)


#%% Calculate intentional binding (IB) effects
# Assuming conditions are named as "IB-press", "IB-tone", "IB-singlePress", "IB-singleTone"
if (all(c("IB-press", "IB-tone", "IB-singlePress", "IB-singleTone") %in% agg.data$condition_clean)) {
  # Filter to only include subjects with complete data
  complete_subject_ids <- complete_subjects$id[complete_subjects$present]
  agg.data.complete <- agg.data[agg.data$id %in% complete_subject_ids, ]
  
  if (nrow(agg.data.complete) > 0) {
    ib_data <- reshape(agg.data.complete, idvar = "id", timevar = "condition_clean", direction = "wide")
    ib_data$IB_press <- ib_data$`meanErrTime.IB-press` - ib_data$`meanErrTime.IB-singlePress`
    ib_data$IB_tone <- ib_data$`meanErrTime.IB-tone` - ib_data$`meanErrTime.IB-singleTone`
    ib_data <- ib_data[, c("id", "IB_press", "IB_tone")]
    cat("IB effects calculated for", nrow(ib_data), "subjects with complete data.\n")
  } else {
    warning("No subjects have complete data for all conditions.")
    ib_data <- data.frame()
  }
} else {
  warning("Not all required conditions for IB calculation are present in the data.")
  ib_data <- data.frame() # Empty data frame if conditions are missing
}
