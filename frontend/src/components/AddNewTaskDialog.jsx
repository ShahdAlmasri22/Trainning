import {
    Button, Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    InputLabel,
    MenuItem,
    Select,
    TextField
} from "@mui/material";


export default function AddNewTaskDialog(
    {
        open,
        setOpen,
        title,
        setTitle,
        description,
        setDescription,
        priority,
        setPriority,
        createTaskMutation
    }
){
    return(
    <>
    <Dialog open={open} onClose={() => setOpen(false)}>
        <DialogTitle sx={{ display: "flex", justifyContent: "space-between" }}>
          Add New Task

        <Button onClick={() => setOpen(false)} sx={{ minWidth: 0, color: "gray", fontSize: "13px", }}>
          ✕
        </Button>
        </DialogTitle>

        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Task Title"
            fullWidth
            value={title}
            sx={{
              mb: 1,
                fontSize: "10px",
            }}
            size="small"
            onChange={(e) => setTitle(e.target.value)}
          />

          <TextField
          margin="dense"
          label="Task Description"
          fullWidth
          value={description}
          sx={{
            mb: 2,
            fontSize: "10px",
          }}
          size="small"
          onChange={(e) => setDescription(e.target.value)}
        />

        <FormControl fullWidth size="small">
        <InputLabel>Priority</InputLabel>
        <Select
          value={priority}
          label="priority"
          size="small"
          onChange={(e) => setPriority(e.target.value)}
          sx={{ fontSize: "13px" }}
        >
          <MenuItem value="LOW">LOW</MenuItem>
          <MenuItem value="MEDIUM">MEDIUM</MenuItem>
          <MenuItem value="HIGH">HIGH</MenuItem>
        </Select>
        </FormControl>
        </DialogContent>

        <DialogActions>
          <Button onClick={() => setOpen(false)}>Cancel</Button>

          <Button
            onClick={() => {
              createTaskMutation.mutate({
                title: title,
                description: description,
                priority: priority,
              });
            }}
             disabled={createTaskMutation.isPending}
          >
              {createTaskMutation.isPending ? "Adding..." : "Add\n"}
          </Button>
        </DialogActions>
    </Dialog>
        </>
    );
}
