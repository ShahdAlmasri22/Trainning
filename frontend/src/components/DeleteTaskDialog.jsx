import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Typography,
} from "@mui/material";

export default function DeleteTaskDialog({
  open,
  setOpen,
  handleDelete,
  deleteTaskMutation
}) {
  return (
  <Dialog open={open} onClose={() => setOpen(false)}>
      <DialogTitle>Confirm Delete</DialogTitle>

          <DialogContent>
            <Typography >
              Are you sure you want to delete this task?
            </Typography>
          </DialogContent>

          <DialogActions sx={{ mb: 3, mr: 23}}>
            <Button onClick={() => setOpen(false)}
                     size="small"
                  sx={{borderRadius: 5, fontSize: 11}}
            >
              Cancel
            </Button>

            <Button
              color="error"
              variant="contained"
               size="small"
              onClick={handleDelete}
              sx={{borderRadius: 5, fontSize: 11}}
              disabled={deleteTaskMutation.isPending}
            >
           {deleteTaskMutation.isPending ? "Deleting..." : "Delete"}
        </Button>
      </DialogActions>
  </Dialog>
  );
}