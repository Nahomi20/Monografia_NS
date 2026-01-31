using Microsoft.AspNetCore.Mvc;

namespace GestionAcademica.Controllers.Dashboard
{
    public class DashboardController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
