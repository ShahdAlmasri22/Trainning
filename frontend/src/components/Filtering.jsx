import {FormControl, InputLabel, MenuItem, Select, Typography} from "@mui/material";


export default function Filtering(
    {
       filterPriority,
       setFilterPriority,
       setSkip,
       filterStatus,
       setFilterStatus
    }
){
    return(
        <>
        <Typography
            sx={{
              fontSize: "16px",
              fontWeight: 500,
              color: "black",
            }}
        >
          Filter by
        </Typography>
        <FormControl
           size="small"
            sx={{
              minWidth: 150,
              borderRadius: 3,
              boxShadow: 3,
            }}
        >
        <InputLabel shrink>Priority</InputLabel>
        <Select
          value={filterPriority}
          label="Priority"
          onChange={(e) => {
            setFilterPriority(e.target.value);
            setSkip(0);
          }}
          displayEmpty
          sx={{
            borderRadius: 3,
          }}
        >
          <MenuItem value="">All Priority</MenuItem>
          <MenuItem value="LOW">Low</MenuItem>
          <MenuItem value="MEDIUM">Medium</MenuItem>
          <MenuItem value="HIGH">High</MenuItem>
        </Select>
        </FormControl>


        <FormControl
          size="small"
          sx={{
            minWidth: 150,
            borderRadius: 3,
            boxShadow: 3,
            ml: 2,
          }}
        >
        <InputLabel shrink>Status</InputLabel>
        <Select
          value={filterStatus}
          label="Status"
          displayEmpty
          onChange={(e) => {
            setFilterStatus(e.target.value);
            setSkip(0);
          }}
          sx={{
            borderRadius: 3,
          }}
        >
          <MenuItem value="">All Status</MenuItem>
          <MenuItem value="PENDING">Pending</MenuItem>
          <MenuItem value="RUNNING">Running</MenuItem>
          <MenuItem value="COMPLETED">Completed</MenuItem>
        </Select>
        </FormControl>
        </>
    );
}
