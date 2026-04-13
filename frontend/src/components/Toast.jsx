import {Alert, Snackbar} from "@mui/material";


export default function Toast(
    {
        toast,
        setToast
    }
){
    return(
        <>
            <Snackbar
          open={toast.open}
          autoHideDuration={3000}
          onClose={() => setToast(prev => ({ ...prev, open: false }))}
          anchorOrigin={{ vertical: "top", horizontal: "center" }}
        >
          <Alert
            severity={toast.severity}
            onClose={() => setToast(prev => ({ ...prev, open: false }))}
            variant="filled"
            sx={{ width: "100%" }}
          >
            {toast.message}
          </Alert>
        </Snackbar>
        </>
    );
}
