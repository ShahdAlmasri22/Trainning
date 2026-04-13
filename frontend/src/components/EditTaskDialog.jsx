import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";

export default function EditTaskDialog({
  open,
  setOpen,
  editTitle,
  setEditTitle,
  editDesc,
  setEditDesc,
  editPriority,
  setEditPriority,
  editStatus,
  setEditStatus,
  handleUpdate,
  updateTaskMutation
}) {
  return (
     <Dialog open={open} onClose={() => setOpen(false)} fullWidth>
        <DialogTitle sx={{ display: "flex", justifyContent: "space-between" }}>
          Edit Task

          <Button onClick={() => setOpen(false)} sx={{ minWidth: 0, color: "gray", fontSize: "13px" }}>
            ✕
          </Button>
        </DialogTitle>
        <DialogContent>
            <TextField
              fullWidth
              size="small"
              margin="dense"
              label="Title"
              sx={{
                mb: 1.5,
                "& input": {
                  fontSize: "13px",
                },
              }}
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
            />

            <TextField
              fullWidth
              size="small"
              margin="dense"
              label="Description"
              sx={{
                mb: 2,
                "& input": {
                  fontSize: "13px",
                },
              }}
              value={editDesc}
              onChange={(e) => setEditDesc(e.target.value)}
            />

            <FormControl fullWidth size="small" sx={{ mb: 1.5 }}>
              <InputLabel>Priority</InputLabel>
              <Select
                value={editPriority}
                label="Priority"
                onChange={(e) => setEditPriority(e.target.value)}
                sx={{ fontSize: "13px", mb: 1 }}
              >
                <MenuItem value="LOW">LOW</MenuItem>
                <MenuItem value="MEDIUM">MEDIUM</MenuItem>
                <MenuItem value="HIGH">HIGH</MenuItem>
              </Select>
            </FormControl>

            <FormControl fullWidth size="small">
              <InputLabel>Status</InputLabel>
              <Select
                value={editStatus}
                label="Status"
                onChange={(e) => setEditStatus(e.target.value)}
                sx={{ fontSize: "13px" }}
              >
            <MenuItem value="PENDING">PENDING</MenuItem>
            <MenuItem value="RUNNING">RUNNING</MenuItem>
            <MenuItem value="COMPLETED">COMPLETED</MenuItem>
          </Select>
        </FormControl>
      </DialogContent>

        <DialogActions sx={{mb:1.5, mr: 54 }}>
          <Button onClick={() => setOpen(false)} sx={{borderRadius: 5, fontSize: 11}}>
            Cancel
          </Button>

          <Button variant="contained" onClick={handleUpdate} sx={{borderRadius: 5, fontSize: 11}}
          disabled={updateTaskMutation.isPending}
          >
            {updateTaskMutation.isPending ? "Saving..." : "Save"}
          </Button>
      </DialogActions>
    </Dialog>
      );
}