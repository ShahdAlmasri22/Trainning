import {FormControl, InputLabel, MenuItem, Select} from "@mui/material";


export default function Sorting(
    {
        sortBy,
        setSortBy,
        order,
        setOrder
    }
){
    return(
        <>
        <FormControl
          size="small"
          sx={{
            minWidth: 160,
            background: "#ffffff",
            borderRadius: 3,
            boxShadow: 2,
            mt:2,
            ml:2
          }}
        >
        <InputLabel>Sort by</InputLabel>
        <Select
          value={sortBy}
          label="Sort by"
          onChange={(e) => setSortBy(e.target.value)}
          sx={{
            borderRadius: 3,
          }}
        >
          <MenuItem value="created_at">Newest</MenuItem>
          <MenuItem value="priority">Priority</MenuItem>
          <MenuItem value="status">Status</MenuItem>
          <MenuItem value="title">Title</MenuItem>
        </Select>
        </FormControl>

        <FormControl
          size="small"
          sx={{
            minWidth: 140,
            background: "#ffffff",
            borderRadius: 3,
            boxShadow: 2,
            mt:2,
            ml:2,
          }}
        >
        <InputLabel>Order</InputLabel>
        <Select
          value={order}
          label="Order"
          onChange={(e) => setOrder(e.target.value)}
          sx={{
            borderRadius: 3,
          }}
        >
          <MenuItem value="desc" >Desc</MenuItem>
          <MenuItem value="asc">Asc</MenuItem>
        </Select>
    </FormControl>
        </>
    );
}
